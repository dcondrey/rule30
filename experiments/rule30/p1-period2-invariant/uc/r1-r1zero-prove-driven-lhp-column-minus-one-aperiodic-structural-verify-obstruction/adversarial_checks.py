"""Adversarial checks for PROOF.md of lemma driven-lhp-column-minus-one-aperiodic (structural form).

Independent code: no import from the proof directory.  Rows are Python ints with bit i = s(t,-i);
bit 0 is the boundary column c_t (overwritten every step).  Convention of this repo:
Rule 30  s(t+1,x) = s(t,x-1) XOR (s(t,x) OR s(t,x+1))
Rule 90  s(t+1,x) = s(t,x-1) XOR s(t,x+1)
Rule 60  s(t+1,x) = s(t,x-1) XOR s(t,x)          (left permutive, but f(0,0,1) = 0: (F1) FAILS)
Rule 150 s(t+1,x) = s(t,x-1) XOR s(t,x) XOR s(t,x+1)   ((F0),(F1),(LP) all hold)

Checks
  A1  Theorem 1 counterexample search, Rules 30/90/150 (theorem applies) and Rule 60 (control, (F1) fails):
      all y on x = -1..-6 (64, including y = 0), c = prefix + w^omega, primitive w of period 1..5,
      prefix length 0..1, (ND) enforced, T = 2048; a hit is an l that is q-periodic on [T/2, T] for some
      q <= 256.  Theorem 1 predicts 0 hits for 30/90/150; Rule 60 must produce hits or the test cannot fire.
  A2  Theorem 2 pairwise check, Rules 30/90 and Rule 60 control: y on x = -1..-5 (32), pure periodic w of
      period 1..4, T = 1024, columns -1..-6; count runs in which two or more columns are q-periodic on
      [T/2, T] for some q <= 64.
  A3  Rule 90 filter on Proposition A, on the one instance where its antecedent is TRUE: the Rule 90
      lone seed has c = 1 0^omega (eventually periodic).  Check Z infinite (|Z| = T), r|Z has ones exactly
      at t = 2^j - 1, and r|Z has no period q <= 256 on [T/2, T].  Prop A's analogue must hold here.
  A4  Necessity of (ND): y = 0 (equivalently y = delta_0, which the lemma text calls 'nonzero finite')
      with c = 0^omega gives l = 0^omega, periodic.  The lemma as worded is false there.
  A5  Rule 90 transport of Corollary A.1: (R1_90) and (P1_90) are both false on the Rule 90 lone seed,
      consistent with (R1) <=> (P1); the argument proves nothing false for Rule 90.

usage: cd <kernel dir> && uv run python uc/<this dir>/adversarial_checks.py > uc/<this dir>/adversarial_checks.log
"""
import itertools
import sys
import time

sys.path.insert(0, '/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-r1zero')
from r1zero_lib import lone_seed_columns, rule90_step  # only for A3 (true Rule 90 diagram)


def step_fn(rule):
    if rule == 30:
        return lambda row: (row >> 1) ^ (row | (row << 1))
    if rule == 90:
        return lambda row: (row >> 1) ^ (row << 1)
    if rule == 60:
        # s(t+1,x) = s(t,x-1) XOR s(t,x); mirrored index i = -x: new[i] = old[i+1] XOR old[i]
        return lambda row: (row >> 1) ^ row
    if rule == 150:
        return lambda row: (row >> 1) ^ row ^ (row << 1)
    raise ValueError(rule)


def lhp_column_minus_one(rule, y_int, c, T):
    """Return bytes l[0..T] with l[t] = s(t,-1), plus the list of column bytes for columns -1..-6."""
    st = step_fn(rule)
    row = (y_int & ~1) | c[0]
    cols = [bytearray(T + 1) for _ in range(6)]
    for t in range(T + 1):
        for i in range(6):
            cols[i][t] = (row >> (i + 1)) & 1
        row = (st(row) & ~1) | c[t + 1]
    return cols


def periodic_on_tail(col, T, qmax):
    """Smallest q <= qmax with col[i] == col[i+q] for all i in [T//2, T-q]; None if none."""
    h = T // 2
    b = bytes(col)
    for q in range(1, qmax + 1):
        if b[h:T + 1 - q] == b[h + q:T + 1]:
            return q
    return None


def primitive_words(pmax):
    words = []
    for p in range(1, pmax + 1):
        for bits in itertools.product((0, 1), repeat=p):
            w = list(bits)
            if 1 not in w:
                continue
            if any(p % d == 0 and w == w[:d] * (p // d) for d in range(1, p)):
                continue
            words.append(w)
    return words


def drives(pmax, prefmax, length):
    out = []
    for w in primitive_words(pmax):
        for L in range(prefmax + 1):
            for pref in itertools.product((0, 1), repeat=L):
                c = list(pref) + [w[k % len(w)] for k in range(length)]
                out.append((w, list(pref), c))
    return out


def check_a1():
    T = 2048
    D = drives(5, 1, T + 3)
    for rule in (30, 90, 150, 60):
        runs = 0
        hits = 0
        example = None
        t0 = time.time()
        for y in range(64):
            y_int = y << 1
            for w, pref, c in D:
                if y_int == 0 and 1 not in c:
                    continue
                runs += 1
                cols = lhp_column_minus_one(rule, y_int, c, T)
                q = periodic_on_tail(cols[0], T, 256)
                if q is not None:
                    hits += 1
                    if example is None:
                        example = (y, w, pref, q)
        print(f"CHECK A1 rule {rule}: Theorem 1 counterexample search, y on x=-1..-6 (64) x drives "
              f"(primitive w period 1..5, prefix 0..1) = {len(D)}, (ND) enforced, T={T}, q<=256 on [T/2,T]: "
              f"runs={runs} hits={hits} first_hit={example} [{time.time() - t0:.0f}s]", flush=True)


def check_a2():
    T = 1024
    for rule in (30, 90, 60):
        runs = 0
        multi = 0
        example = None
        for y in range(32):
            y_int = y << 1
            for w in primitive_words(4):
                c = [w[k % len(w)] for k in range(T + 3)]
                runs += 1
                cols = lhp_column_minus_one(rule, y_int, c, T)
                per = [periodic_on_tail(col, T, 64) for col in cols]
                k = sum(1 for q in per if q is not None)
                if k >= 2:
                    multi += 1
                    if example is None:
                        example = (y, w, per)
        print(f"CHECK A2 rule {rule}: Theorem 2 pairwise, y on x=-1..-5 (32) x pure periodic w period 1..4, T={T}, "
              f"columns -1..-6, q<=64 on [T/2,T]: runs={runs} runs_with_two_or_more_periodic_columns={multi} "
              f"example={example}", flush=True)


def check_a3():
    T = 4096
    cols = lone_seed_columns(T, [0, 1, -1], step=rule90_step)
    c = cols[0]
    r = cols[1]
    l = cols[-1]
    c_period = periodic_on_tail(bytes(c), T, 256)
    Z = [t for t in range(T + 1) if c[t] == 0]
    rZ = bytes(r[t] for t in Z)
    ones = [Z[k] for k in range(len(Z)) if rZ[k]]
    expect = [(1 << j) - 1 for j in range(1, 13)]
    rz_period = periodic_on_tail(rZ, len(Z) - 1, 256)
    l_period = periodic_on_tail(bytes(l), T, 256)
    print(f"CHECK A3 Rule 90 lone seed, T={T}: c eventually periodic (q on tail)={c_period}; |Z|={len(Z)} "
          f"(= T, Z infinite); ones of r|Z at times {ones[:6]}... == 2^j-1: {ones == expect}; "
          f"r|Z period q<=256 on tail: {rz_period}; l period q<=256 on tail: {l_period}; "
          f"Prop A analogue holds on this instance: {c_period is not None and rz_period is None}", flush=True)
    return c_period, rz_period


def check_a4():
    T = 256
    c = [0] * (T + 3)
    cols = lhp_column_minus_one(30, 0, c, T)
    q = periodic_on_tail(cols[0], T, 4)
    print(f"CHECK A4 (ND) necessity: y = 0 on x<=-1 (the lone-seed y = delta_0 restricted), c = 0^omega, Rule 30, "
          f"T={T}: sum(l)={sum(cols[0])} l periodic with q={q}; lemma text 'nonzero finite y' is insufficient: "
          f"{q is not None}", flush=True)


def check_a5(c_period, rz_period):
    p1_90 = c_period is None
    r1_90 = (c_period is None) or (rz_period is not None)
    print(f"CHECK A5 Rule 90 transport of Corollary A.1: P1_90 (c aperiodic) = {p1_90}; R1_90 ('c periodic => r|Z "
          f"periodic') = {r1_90}; equivalence R1_90 <=> P1_90 consistent: {p1_90 == r1_90}; nothing false is proved", flush=True)


def main():
    t0 = time.time()
    print("adversarial_checks.py: independent checks on PROOF.md (structural), lemma driven-lhp-column-minus-one-aperiodic")
    check_a1()
    check_a2()
    cp, rz = check_a3()
    check_a4()
    check_a5(cp, rz)
    print(f"DONE [{time.time() - t0:.0f}s]")


if __name__ == '__main__':
    main()
