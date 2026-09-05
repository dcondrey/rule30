"""Finite checks backing PROOF.md (lemma driven-lhp-column-minus-one-aperiodic).

Every check here is a gate on an identity or a construction that PROOF.md also derives in full;
none of them is a proof step in itself.  Each prints a line 'CHECK <name>: ... mismatches=<k>'.

Conventions (this repo): s(t+1,x) = s(t,x-1) XOR (s(t,x) OR s(t,x+1)) for Rule 30,
s(t+1,x) = s(t,x-1) XOR s(t,x+1) for Rule 90.  Left half-plane rows are Python ints with
bit i = s(t,-i); bit 0 is the boundary column c_t.

Checks
  G1  back-solve identity a = d XOR g(b,c) with d = a XOR g(b,c), all 8 triples, both rules
  G2  moving edge m_(t+1) = m_t - 1 once the support is nonempty: exhaustive over all y on
      x = -1..-6 and all period-8 drives, T = 40, both rules; plus random y, random c, T = 200
  G3  back-solve reconstruction of the whole driven half-plane from columns 0 and -1
  G4  true lone-seed diagram restricted to x <= 0 equals LHP_seed(c*), x >= 1 equals RHP_seed(c*),
      and the x = 0 rule splits into the pin (c_t = 1) and the coupling (c_t = 0), T = 4096
  G5  assembly uniqueness: among all c in {0,1}^(T+1) with c_0 = 1, exactly one satisfies the
      x = 0 rule at every t < T with l, r from the driven half-planes, and it is c*; T = 12
  G6  Rule 90 instance: LHP_seed(1 0^inf) column -1 is [t = 2^j - 1], T = 4096
  G7  instances of Theorem 1 outside the screened family: c = 0^omega with y = {-1}; c = 0^omega
      with y = {-3, -1}; no eventual period q <= 256 with onset <= T/2 at T = 4096

usage: uv run python verify_driven_lhp.py > verify_driven_lhp.log
"""
import sys, itertools, random, time

sys.path.insert(0, '/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-r1zero')
from r1zero_lib import lone_seed_rows, rule30_step, eventual_period, longest_shift_agreement

OUT = []


def say(s):
    OUT.append(s)
    print(s, flush=True)


def g30(b, c):
    return b | c


def g90(b, c):
    return c


RULES = {'30': g30, '90': g90}


def f(rule, a, b, c):
    return a ^ RULES[rule](b, c)


# ---------- explicit cell-array driven left half-plane (reference) ----------
def lhp_cells(rule, y_cells, c, T):
    """y_cells[i] = s(0,-i) for i >= 1 (index 0 ignored); c[t] = s(t,0).  Returns rows[t][i] = s(t,-i)."""
    W = T + len(y_cells) + 4
    row = [0] * W
    for i in range(1, len(y_cells)):
        row[i] = y_cells[i]
    row[0] = c[0]
    rows = []
    for t in range(T + 1):
        rows.append(row)
        new = [0] * W
        for i in range(1, W - 1):
            # x = -i; left neighbour x-1 is index i+1, right neighbour x+1 is index i-1
            new[i] = f(rule, row[i + 1], row[i], row[i - 1])
        new[0] = c[t + 1]
        row = new
    return rows


# ---------- int-row driven half-planes ----------
def lhp_step(rule, row, ct1):
    if rule == '30':
        nxt = (row >> 1) ^ (row | (row << 1))
    else:
        nxt = (row >> 1) ^ (row << 1)
    return (nxt & ~1) | ct1


def lhp_ints(rule, y_int, c, T):
    """y_int has bit i = s(0,-i) for i >= 1.  Returns list of int rows, bit i = s(t,-i)."""
    row = (y_int & ~1) | c[0]
    rows = []
    for t in range(T + 1):
        rows.append(row)
        row = lhp_step(rule, row, c[t + 1])
    return rows


def rhp_step30(row, ct1):
    # bit x = s(t,x) for x >= 0; s(t+1,x) = s(t,x-1) XOR (s(t,x) OR s(t,x+1))
    nxt = (row << 1) ^ (row | (row >> 1))
    return (nxt & ~1) | ct1


def rhp_ints30(c, T):
    row = c[0]
    rows = []
    for t in range(T + 1):
        rows.append(row)
        row = rhp_step30(row, c[t + 1])
    return rows


# ---------- G1 ----------
def check_g1():
    bad = 0
    for rule in ('30', '90'):
        for a, b, c in itertools.product((0, 1), repeat=3):
            d = f(rule, a, b, c)
            if (d ^ RULES[rule](b, c)) != a:
                bad += 1
    say(f"CHECK G1 back-solve identity a = d XOR g(b,c), 16 cases (8 triples x 2 rules): mismatches={bad}")
    return bad


# ---------- G2 ----------
def edge_violations(rule, y_int, c, T):
    """Count t >= t0 with m_t != a - (t - t0).  Mirrored: m_t = -(bit_length - 1) when row != 0."""
    rows = lhp_ints(rule, y_int, c, T)
    t0 = None
    for t, row in enumerate(rows):
        if row:
            t0 = t
            top0 = row.bit_length() - 1
            break
    if t0 is None:
        return 0, None
    viol = 0
    for t in range(t0, T + 1):
        row = rows[t]
        if row == 0 or row.bit_length() - 1 != top0 + (t - t0):
            viol += 1
    return viol, t0


def check_g2():
    total = 0
    viol = 0
    T = 40
    for rule in ('30', '90'):
        for ybits in range(64):
            y_int = ybits << 1          # bits 1..6 = s(0,-1..-6)
            for pref in range(256):
                w = [(pref >> k) & 1 for k in range(8)]
                c = [w[t % 8] for t in range(T + 2)]
                if y_int == 0 and pref == 0:
                    continue            # degenerate: identically zero half-plane, excluded by (ND)
                v, t0 = edge_violations(rule, y_int, c, T)
                total += 1
                viol += v
    say(f"CHECK G2a moving edge, exhaustive y on x=-1..-6 (64) x period-8 drives (256) x 2 rules, T={T}: "
        f"runs={total} edge violations={viol}")
    rng = random.Random(20260903)
    total = 0
    viol = 0
    T = 200
    for rule in ('30', '90'):
        for _ in range(500):
            width = rng.randint(1, 24)
            y_int = rng.getrandbits(width) << 1
            c = [rng.getrandbits(1) for _ in range(T + 2)]
            if y_int == 0 and 1 not in c:
                continue
            v, t0 = edge_violations(rule, y_int, c, T)
            total += 1
            viol += v
    say(f"CHECK G2b moving edge, random y (width<=24) and random aperiodic c, T={T}, 2 rules: runs={total} "
        f"edge violations={viol}")
    # gate the int kernel against the cell-array reference on a random subset
    bad = 0
    cells = 0
    for rule in ('30', '90'):
        for _ in range(30):
            width = rng.randint(1, 10)
            ybits = [0] + [rng.getrandbits(1) for _ in range(width)]
            c = [rng.getrandbits(1) for _ in range(50)]
            ref = lhp_cells(rule, ybits, c, 40)
            y_int = sum(b << i for i, b in enumerate(ybits))
            got = lhp_ints(rule, y_int, c, 40)
            for t in range(41):
                for i in range(len(ref[t])):
                    cells += 1
                    if ref[t][i] != ((got[t] >> i) & 1):
                        bad += 1
    say(f"CHECK G2c int kernel vs cell-array reference, 60 random (y,c), 2 rules: cells={cells} mismatches={bad}")
    return viol + bad


# ---------- G3 ----------
def check_g3():
    rng = random.Random(7)
    bad = 0
    cells = 0
    T = 300
    K = 60
    for _ in range(40):
        width = rng.randint(0, 20)
        y_int = rng.getrandbits(width) << 1 if width else 0
        c = [rng.getrandbits(1) for _ in range(T + 2)]
        c[0] = 1
        rows = lhp_ints('30', y_int, c, T)
        s = lambda t, x: (rows[t] >> (-x)) & 1
        # reconstruct s(t, x-1) for x = -1 .. -K from columns x, x+1 at t and column x at t+1
        rec = {}
        for t in range(T):
            rec[(t, 0)] = s(t, 0)
            rec[(t, -1)] = s(t, -1)
        for x in range(-1, -K - 1, -1):
            for t in range(T - K + x + 1):
                if (t + 1, x) not in rec:
                    continue
                rec[(t, x - 1)] = rec[(t + 1, x)] ^ (rec[(t, x)] | rec[(t, x + 1)])
        for (t, x), v in rec.items():
            if x <= -2:
                cells += 1
                if v != s(t, x):
                    bad += 1
    say(f"CHECK G3 back-solve reconstruction of columns -2..-{K+1} from columns 0,-1, 40 random drives, T={T}: "
        f"cells={cells} mismatches={bad}")
    return bad


# ---------- G4 ----------
def check_g4():
    T = 4096
    true_rows = []
    for t, row, off in lone_seed_rows(T):
        true_rows.append((row, off))
    cstar = [(row >> off) & 1 for row, off in true_rows]
    cstar_ext = cstar + [0, 0]   # c_(T+1) is only needed to build row T+1, never compared
    lhp = lhp_ints('30', 0, cstar_ext, T)
    rhp = rhp_ints30(cstar_ext, T)
    bad_l = bad_r = 0
    cells_l = cells_r = 0
    for t in range(T + 1):
        row, off = true_rows[t]
        left = row & ((1 << (off + 1)) - 1)          # bits 0..off hold x = -off..0
        # mirrored: bit i of lhp[t] = s(t,-i); true bit (off - i) = s(t,-i)
        mir = 0
        for i in range(off + 1):
            mir |= ((left >> (off - i)) & 1) << i
        cells_l += off + 1
        bad_l += bin(mir ^ lhp[t]).count('1')
        right = row >> off                             # bit x = s(t,x) for x >= 0
        cells_r += (row.bit_length() - off) if row.bit_length() > off else 1
        bad_r += bin(right ^ rhp[t]).count('1')
    say(f"CHECK G4a true lone-seed diagram x<=0 equals LHP_seed(c*), T={T}: cells={cells_l} mismatches={bad_l}")
    say(f"CHECK G4b true lone-seed diagram x>=1 equals RHP_seed(c*), T={T}: cells={cells_r} mismatches={bad_r}")
    l = [(lhp[t] >> 1) & 1 for t in range(T + 1)]
    r = [(rhp[t] >> 1) & 1 for t in range(T + 1)]
    pin_bad = 0
    pin_n = 0
    cpl_bad = 0
    cpl_n = 0
    for t in range(T):
        if cstar[t] == 1:
            pin_n += 1
            if l[t] != 1 ^ cstar[t + 1]:
                pin_bad += 1
        else:
            cpl_n += 1
            if r[t] != cstar[t + 1] ^ l[t]:
                cpl_bad += 1
    say(f"CHECK G4c pin l*_t = 1 XOR c*_(t+1) at one-times: checked={pin_n} violations={pin_bad}; "
        f"coupling r*_t = c*_(t+1) XOR l*_t at zero-times: checked={cpl_n} violations={cpl_bad}")
    ep_c = eventual_period(cstar, 256)
    ep_l = eventual_period(l, 256)
    say(f"INFO G4d lone seed to T={T}: |Z|={cpl_n + (1 - cstar[T])} eventual_period(c*, q<=256)={ep_c} "
        f"eventual_period(l*, q<=256)={ep_l} (information only; not a proof step)")
    return bad_l + bad_r + pin_bad + cpl_bad


# ---------- G5 ----------
def check_g5():
    T = 12
    cstar = [(row >> off) & 1 for t, row, off in lone_seed_rows(T + 1)]
    n_rule = 0
    n_pin = 0
    sols = []
    for bits in range(1 << T):
        c = [1] + [(bits >> k) & 1 for k in range(T)] + [0]
        lhp = lhp_ints('30', 0, c, T)
        rhp = rhp_ints30(c, T)
        ok_rule = True
        ok_pin = True
        for t in range(T):
            l = (lhp[t] >> 1) & 1
            r = (rhp[t] >> 1) & 1
            if c[t + 1] != (l ^ (c[t] | r)):
                ok_rule = False
            if c[t] == 1 and l != (1 ^ c[t + 1]):
                ok_pin = False
        n_rule += ok_rule
        n_pin += ok_pin
        if ok_rule:
            sols.append(c[:T + 1])
    match = (len(sols) == 1 and sols[0] == cstar[:T + 1])
    say(f"CHECK G5 assembly uniqueness, T={T}, all 2^{T} words with c_0=1: words satisfying the x=0 rule at "
        f"every t<T: {n_rule}; equal to c*[:{T + 1}]: {match}; words satisfying only the pin: {n_pin} (information)")
    return 0 if match else 1


# ---------- G6 ----------
def check_g6():
    T = 4096
    c = [1] + [0] * (T + 2)
    rows = lhp_ints('90', 0, c, T)
    l = [(rows[t] >> 1) & 1 for t in range(T + 1)]
    ones = [t for t in range(T + 1) if l[t]]
    expect = [(1 << j) - 1 for j in range(1, 14) if (1 << j) - 1 <= T]
    v, t0 = edge_violations('90', 0, c, T)
    say(f"CHECK G6 Rule 90 LHP_seed(1 0^inf) column -1: ones at {ones[:8]}... equals 2^j-1: {ones == expect}; "
        f"eventual_period(q<=256)={eventual_period(l, 256)}; edge violations={v}")
    return 0 if ones == expect and v == 0 else 1


# ---------- G7 ----------
def check_g7():
    T = 4096
    res = 0
    for name, y_int in (("y={-1}", 1 << 1), ("y={-3,-1}", (1 << 3) | (1 << 1))):
        c = [0] * (T + 2)
        rows = lhp_ints('30', y_int, c, T)
        l = [(rows[t] >> 1) & 1 for t in range(T + 1)]
        ep = eventual_period(l, 256)
        run, q, i0 = longest_shift_agreement(l, 256)
        v, t0 = edge_violations('30', y_int, c, T)
        say(f"CHECK G7 Theorem 1 instance c=0^omega, {name}, T={T}: ones(l)={sum(l)} eventual_period(q<=256, "
            f"onset<=T/2)={ep} longest shift-agreement run={run} at shift {q} (random null log2(T*256)=20.0) "
            f"edge violations={v}")
        res += (ep is not None) + v
    return res


def main():
    t0 = time.time()
    say("verify_driven_lhp.py: finite gates for PROOF.md, lemma driven-lhp-column-minus-one-aperiodic")
    total = 0
    total += check_g1()
    total += check_g2()
    total += check_g3()
    total += check_g4()
    total += check_g5()
    total += check_g6()
    total += check_g7()
    say(f"FINAL: total mismatches/violations across G1..G7 = {total}; verdict {'PASS' if total == 0 else 'FAIL'} "
        f"[{time.time() - t0:.1f}s]")


if __name__ == '__main__':
    main()
