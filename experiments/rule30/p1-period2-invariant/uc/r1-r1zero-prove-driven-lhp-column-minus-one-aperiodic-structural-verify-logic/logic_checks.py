"""Logic-lens validation checks for PROOF.md (lemma driven-lhp-column-minus-one-aperiodic).

None of these is a proof step.  They pin the three points the verdict raises:

  L1  The lemma's literal hypothesis "nonzero finite y" is insufficient: y = delta_0 is nonzero
      and finite, c = 0^omega is eventually periodic, and the driven half-plane is identically
      zero, so l = 0^omega is periodic.  PROOF.md's replacement hypothesis (ND) is required.
  L2  Instance check of Theorem 2 (no column x <= -1 eventually periodic for eventually periodic
      c): random y, random eventually periodic c with period 1..6 and prefix 0..8, columns
      -1..-8, T = 2048, eventual period q <= 128 with onset <= T/2.
  L3  Instance check of Lemma 7's enumeration identity z_(k+k_p) = z_k + p for k >= k_0 on
      random eventually periodic c with infinite zero set.
  L4  Instance of the Rule 90 remark in PROOF.md section 8: lone-seed Rule 90 has c* = 1 0^omega,
      l*_t = c*_(t+1) XOR r*_t at every t, and r* = [t = 2^j - 1].

usage: cd <p1-period2-invariant> && uv run python uc/<this dir>/logic_checks.py > uc/<this dir>/logic_checks.log
"""
import sys, random, time

sys.path.insert(0, '/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-r1zero')
from r1zero_lib import lone_seed_rows, rule90_step, eventual_period


def say(s):
    print(s, flush=True)


def lhp_step(rule, row, ct1):
    if rule == '30':
        nxt = (row >> 1) ^ (row | (row << 1))
    else:
        nxt = (row >> 1) ^ (row << 1)
    return (nxt & ~1) | ct1


def lhp_ints(rule, y_int, c, T):
    row = (y_int & ~1) | c[0]
    rows = []
    for t in range(T + 1):
        rows.append(row)
        row = lhp_step(rule, row, c[t + 1])
    return rows


def ev_periodic_word(rng, T, p=None, pre=None):
    p = p if p is not None else rng.randint(1, 6)
    pre = pre if pre is not None else rng.randint(0, 8)
    prefix = [rng.getrandbits(1) for _ in range(pre)]
    block = [rng.getrandbits(1) for _ in range(p)]
    c = prefix + [block[(t - pre) % p] for t in range(pre, T + 2)]
    return c, p, pre, block


# ---------- L1 ----------
def check_l1():
    T = 512
    c = [0] * (T + 2)
    rows = lhp_ints('30', 0, c, T)          # y = delta_0: zero on x <= -1 (bit 0 is overwritten by c_0)
    l = [(rows[t] >> 1) & 1 for t in range(T + 1)]
    allzero = all(r == 0 for r in rows)
    ep = eventual_period(l, 4)
    say(f"CHECK L1 y=delta_0 (nonzero, finite), c=0^omega, T={T}: half-plane identically zero={allzero}; "
        f"l eventually periodic (q,onset)={ep}; lemma's literal hypothesis is insufficient={allzero and ep is not None}")
    # and the same with y having its 1 at x = 0 only, c_0 = 0: y(0) is overwritten by c_0
    return 0


# ---------- L2 ----------
def check_l2():
    rng = random.Random(20260903)
    T = 2048
    runs = 0
    periodic_cols = 0
    for _ in range(200):
        width = rng.randint(0, 12)
        y_int = (rng.getrandbits(width) << 1) if width else 0
        c, p, pre, block = ev_periodic_word(rng, T)
        if y_int == 0 and 1 not in c:
            continue
        rows = lhp_ints('30', y_int, c, T)
        runs += 1
        for x in range(1, 9):
            col = [(rows[t] >> x) & 1 for t in range(T + 1)]
            if eventual_period(col, 128) is not None:
                periodic_cols += 1
                say(f"  L2 HIT: y={y_int:#x} p={p} pre={pre} block={block} column -{x} eventual period {eventual_period(col, 128)}")
    say(f"CHECK L2 Theorem 2 instances: random y (width<=12), random eventually periodic c (p<=6, prefix<=8), "
        f"columns -1..-8, T={T}, q<=128, onset<=T/2: runs={runs} eventually periodic columns found={periodic_cols}")
    return periodic_cols


# ---------- L3 ----------
def check_l3():
    rng = random.Random(7)
    T = 4096
    runs = 0
    bad = 0
    for _ in range(300):
        c, p, pre, block = ev_periodic_word(rng, T)
        if 0 not in block:
            continue                        # Z finite: Lemma 7 does not apply
        t_c = pre
        Z = [t for t in range(T + 1) if c[t] == 0]
        k_p = sum(1 for t in range(t_c, t_c + p) if c[t] == 0)
        k_0 = next(k for k, z in enumerate(Z) if z >= t_c)
        runs += 1
        for k in range(k_0, len(Z) - k_p):
            if Z[k + k_p] != Z[k] + p:
                bad += 1
                break
    say(f"CHECK L3 Lemma 7 enumeration identity z_(k+k_p) = z_k + p for k >= k_0, T={T}: runs={runs} violations={bad}")
    return bad


# ---------- L4 ----------
def check_l4():
    T = 2048
    cols = {x: [] for x in (-1, 0, 1)}
    for t, row, off in lone_seed_rows(T, rule90_step):
        for x in cols:
            cols[x].append((row >> (off + x)) & 1)
    c, l, r = cols[0], cols[-1], cols[1]
    id_ok = all(l[t] == (c[t + 1] ^ r[t]) for t in range(T))
    ones_r = [t for t in range(T + 1) if r[t]]
    expect = [(1 << j) - 1 for j in range(1, 13) if (1 << j) - 1 <= T]
    say(f"INFO L4 Rule 90 lone seed, T={T}: c*=1 0^omega: {c[:1] == [1] and 1 not in c[1:]}; "
        f"l*_t = c*_(t+1) XOR r*_t at every t<T: {id_ok}; ones(r*) = 2^j-1: {ones_r == expect}; "
        f"eventual_period(c*, q<=4)={eventual_period(c, 4)} eventual_period(r*, q<=256)={eventual_period(r, 256)}")
    return 0


def main():
    t0 = time.time()
    say("logic_checks.py: validation for the logic verdict on PROOF.md (driven-lhp-column-minus-one-aperiodic)")
    total = check_l1() + check_l2() + check_l3() + check_l4()
    say(f"FINAL: L2 periodic columns + L3 violations = {total} [{time.time() - t0:.1f}s]")


if __name__ == '__main__':
    main()
