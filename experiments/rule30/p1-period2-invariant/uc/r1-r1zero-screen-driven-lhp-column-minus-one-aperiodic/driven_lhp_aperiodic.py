"""Kill test for lemma driven-lhp-column-minus-one-aperiodic.

Lemma (proved in the prompt): for every nonzero finite y and every eventually
periodic boundary word c, the column l_t = LHP_y(c)(t, -1) of the driven left
half-plane is NOT eventually periodic.

LHP_y(c): cells x <= -1 evolve by Rule 30, s(t+1,x) = s(t,x-1) XOR (s(t,x) OR s(t,x+1)),
reading only x-1, x, x+1 <= 0; the column x = 0 is overwritten with c_t at every t;
initial data at t = 0 is y restricted to x <= -1 (and c_0 at x = 0).

Kill test, as pre-registered:
  (i)  simulate LHP_seed(c) for the 44 drives of driven_halfplane.py and search l for an
       eventual period q <= Q with onset <= T/2.  A hit refutes the proof.
  (ii) check the moving left edge s(t, a-t) = 1, s(t, x) = 0 for x < a-t at every t.
Extensions (all still inside the lemma's hypothesis): T pushed to 2^17 and 2^20, Q to 4096,
primitive words to period 8, random nonzero finite y, columns -1..-8 and l|Z, Rule 90 control.

Mirrored bit convention: bit i of a row holds s(t, -i); bit 0 is c_t.
"""
import sys, itertools, time, random, math
import numpy as np

sys.path.insert(0, '/Volumes/A/researchpapers/13-rule30/experiments/rule30/p1-period2-invariant/uc/r1-r1zero')
from r1zero_lib import driven_lhp as lib_driven_lhp, eventual_period as lib_eventual_period, \
    longest_shift_agreement as lib_longest_run, lone_seed_columns


def step30_mirror(row: int) -> int:
    return (row >> 1) ^ (row | (row << 1))


def step90_mirror(row: int) -> int:
    return (row >> 1) ^ (row << 1)


def driven_lhp_y(y: int, c, T: int, ncols: int, step=step30_mirror):
    """Return (cols, edge_violations, rows_kept).

    cols[k][t] = s(t, -k) for k = 0..ncols-1 (k = 0 is c_t itself).
    edge_violations counts t with the moving-edge claim false.
    y is the mirrored initial row (bit i = s(0,-i)); bit 0 is replaced by c[0].
    """
    row = (y & ~1) | c[0]
    # moving edge: a = leftmost 1 of the initial row (mirrored index m = -a), else first t with c_t = 1
    if row:
        m0, t0 = row.bit_length() - 1, 0
    else:
        t0 = next(t for t in range(T + 1) if c[t] == 1)
        m0 = 0
    mask = (1 << ncols) - 1
    packed = np.empty(T + 1, dtype=np.int64)
    edge_viol = 0
    for t in range(T + 1):
        packed[t] = row & mask
        if t >= t0 and row.bit_length() != m0 + (t - t0) + 1:
            edge_viol += 1
        nxt = step(row)
        row = (nxt & ~1) | c[t + 1]
    cols = [((packed >> k) & 1).astype(np.int8) for k in range(ncols)]
    return cols, edge_viol


def reference_lhp_y(y_cells, c, T: int, step_name='30'):
    """Explicit cell-array reference.  y_cells[i] = s(0, -i).  Returns list of rows as lists, index i = s(t,-i)."""
    W = T + len(y_cells) + 4
    row = [0] * W
    for i, v in enumerate(y_cells):
        row[i] = v
    row[0] = c[0]
    rows = []
    for t in range(T + 1):
        rows.append(list(row))
        new = [0] * W
        for i in range(1, W - 1):
            # x = -i: left neighbour x-1 = -(i+1), right neighbour x+1 = -(i-1)
            if step_name == '30':
                new[i] = row[i + 1] ^ (row[i] | row[i - 1])
            else:
                new[i] = row[i + 1] ^ row[i - 1]
        new[0] = c[t + 1]
        row = new
    return rows


def eventual_period_np(seq: np.ndarray, Q: int, min_tail_frac: float = 0.5):
    """Same semantics as r1zero_lib.eventual_period, vectorised."""
    n = len(seq)
    limit = int((1 - min_tail_frac) * n)
    for q in range(1, Q + 1):
        mism = np.flatnonzero(seq[:n - q] != seq[q:])
        onset = 0 if len(mism) == 0 else int(mism[-1]) + 1
        if onset <= limit and n - onset >= 4 * q:
            return q, onset
    return None


def longest_run_np(seq: np.ndarray, Q: int):
    """(run, q, start): longest run of i with seq[i] == seq[i+q], over 1 <= q <= Q."""
    n = len(seq)
    best = (0, 0, 0)
    for q in range(1, Q + 1):
        eq = (seq[:n - q] == seq[q:]).astype(np.int8)
        if not eq.any():
            continue
        d = np.diff(np.concatenate(([0], eq, [0])))
        starts = np.flatnonzero(d == 1)
        ends = np.flatnonzero(d == -1)
        lens = ends - starts
        k = int(lens.argmax())
        if lens[k] > best[0]:
            best = (int(lens[k]), q, int(starts[k]))
    return best


def periodic_words(pmin, pmax):
    words = []
    for p in range(pmin, pmax + 1):
        for bits in itertools.product([0, 1], repeat=p):
            w = list(bits)
            if 1 not in w and p > 1:
                continue
            rots = [tuple(w[i:] + w[:i]) for i in range(p)]
            if tuple(w) != min(rots):
                continue
            if any(p % d == 0 and w == (w[:d] * (p // d)) for d in range(1, p)):
                continue
            words.append(w)
    return words


def build_drive(w, prefix, T):
    p = len(w)
    pl = len(prefix)
    c = list(prefix) + [w[(t - pl) % p] for t in range(pl, T + 2)]
    if c[0] == 0:
        c = [1] + c[1:]
    return c


def gate(out):
    """Gate the fast kernel against the explicit reference and against r1zero_lib."""
    rng = random.Random(7)
    fails = 0
    ncase = 0
    for trial in range(60):
        T = rng.randint(8, 48)
        width = rng.randint(1, 12)
        y_cells = [rng.getrandbits(1) for _ in range(width)]
        c = [rng.getrandbits(1) for _ in range(T + 2)]
        if not any(y_cells) and not any(c):
            c[0] = 1
        y = sum(v << i for i, v in enumerate(y_cells))
        for step_name, step in (('30', step30_mirror), ('90', step90_mirror)):
            ref = reference_lhp_y(y_cells, c, T, step_name)
            cols, ev = driven_lhp_y(y, c, T, 8, step)
            for t in range(T + 1):
                for k in range(8):
                    ncase += 1
                    if cols[k][t] != ref[t][k]:
                        fails += 1
            # moving edge against the reference: leftmost 1 of ref row t
            row0 = [c[0]] + y_cells[1:]
            if any(row0):
                m0, t0 = max(i for i, v in enumerate(row0) if v), 0
            else:
                t0 = next(t for t in range(T + 1) if c[t] == 1)
                m0 = 0
            ev_ref = 0
            for t in range(t0, T + 1):
                ones = [i for i, v in enumerate(ref[t]) if v]
                if not ones or max(ones) != m0 + (t - t0):
                    ev_ref += 1
            if ev != ev_ref:
                fails += 1
            if step_name == '30' and ev_ref != 0:
                out.append(f"  NOTE rule30 reference edge violation count {ev_ref} (T={T}, y={y_cells}, c[:8]={c[:8]})")
    # lib agreement for the seed case (y = 0 apart from c_0)
    lib_fails = 0
    for trial in range(20):
        T = rng.randint(16, 200)
        c = [1] + [rng.getrandbits(1) for _ in range(T + 1)]
        rows = lib_driven_lhp(c, T)
        cols, ev = driven_lhp_y(0, c, T, 8)
        for t in range(T + 1):
            for k in range(8):
                if ((rows[t] >> k) & 1) != cols[k][t]:
                    lib_fails += 1
    # period search gate: planted periods and lib agreement on random sequences
    ps_fails = 0
    for trial in range(200):
        n = rng.randint(64, 400)
        seq = [rng.getrandbits(1) for _ in range(n)]
        if trial % 2 == 0:
            q = rng.randint(1, 12)
            onset = rng.randint(0, n // 3)
            for i in range(onset + q, n):
                seq[i] = seq[i - q]
        a = lib_eventual_period(seq, 32)
        b = eventual_period_np(np.array(seq, dtype=np.int8), 32)
        if a != b:
            ps_fails += 1
        ra = lib_longest_run(seq, 32)
        rb = longest_run_np(np.array(seq, dtype=np.int8), 32)
        if ra[0] != rb[0]:
            ps_fails += 1
    out.append(f"GATE kernel vs explicit reference: {fails} mismatches over {ncase} cells (60 random (y,c) pairs, rules 30 and 90, T<=48)")
    out.append(f"GATE kernel vs r1zero_lib.driven_lhp (seed case): {lib_fails} mismatches over 20 random drives")
    out.append(f"GATE period search vs r1zero_lib: {ps_fails} disagreements over 200 sequences (100 with planted periods)")
    return fails == 0 and lib_fails == 0 and ps_fails == 0


def analyse_drive(label, y, c, T, Q, ncols, out, step=step30_mirror, deep=False):
    """Run one drive, append lines, return dict of findings."""
    t0 = time.time()
    cols, ev = driven_lhp_y(y, c, T, ncols, step)
    l = cols[1]
    carr = cols[0]
    Z = np.flatnonzero(carr[:T + 1] == 0)
    ep_l = eventual_period_np(l, Q)
    run_l = longest_run_np(l, Q)
    ep_lZ = eventual_period_np(l[Z], Q) if len(Z) >= 64 else 'n/a'
    # sharper statement: every single column x <= -1 aperiodic
    col_eps = []
    for k in range(2, ncols):
        col_eps.append(eventual_period_np(cols[k], Q))
    # count of periodic columns among -1..-(ncols-1)
    per_cols = [(-k) for k in range(1, ncols) if eventual_period_np(cols[k], Q) is not None] if not deep else []
    null = math.log2(T * Q)
    out.append(f"{label}: T={T} Q={Q} |Z|={len(Z)} ones(l)={int(l.sum())} "
               f"l eventual_period={ep_l} l|Z eventual_period={ep_lZ} "
               f"longest shift-agreement run={run_l[0]} at shift {run_l[1]} start {run_l[2]} (random null log2(T*Q)={null:.1f}) "
               f"edge violations={ev} periodic columns among -1..-{ncols-1}={per_cols} [{time.time()-t0:.1f}s]")
    return dict(ep_l=ep_l, ep_lZ=ep_lZ, run=run_l[0], ev=ev, per_cols=per_cols)


def main():
    T_main = int(sys.argv[1]) if len(sys.argv) > 1 else 1 << 17
    Q_main = int(sys.argv[2]) if len(sys.argv) > 2 else 1024
    T_deep = int(sys.argv[3]) if len(sys.argv) > 3 else 1 << 20
    Q_deep = int(sys.argv[4]) if len(sys.argv) > 4 else 4096
    out = []
    wall = time.time()
    ok = gate(out)
    out.append(f"GATE overall: {'PASS' if ok else 'FAIL'}")
    print("\n".join(out)); out.clear()
    if not ok:
        return
    true_c = lone_seed_columns(64, [0])[0]
    ncols = 9  # columns 0..-8

    # ---- Part 0: reproduce the T=4096, Q=256 pre-registered census exactly (44 drives)
    words6 = periodic_words(1, 6)
    tally = {}
    for (T, Q, tag) in ((4096, 256, 'REPRO'), (T_main, Q_main, 'MAIN')):
        hits = 0; total = 0; evtot = 0; runs = []; lZ_hits = 0; lZ_total = 0; percol = 0
        for w in words6:
            for pl in (0, 8):
                c = build_drive(w, true_c[:pl], T)
                if sum(1 for t in range(T + 1) if c[t] == 0) < 64:
                    out.append(f"{tag} word {''.join(map(str, w))} prefix_len={pl}: zero set too small, skipped")
                    continue
                r = analyse_drive(f"{tag} word {''.join(map(str, w))} prefix_len={pl}", 0, c, T, Q, ncols, out)
                total += 1; hits += r['ep_l'] is not None; evtot += r['ev']; runs.append(r['run'])
                if r['ep_lZ'] != 'n/a':
                    lZ_total += 1; lZ_hits += r['ep_lZ'] is not None
                percol += len(r['per_cols'])
        out.append(f"SUMMARY {tag} rule30 T={T} Q={Q}: LHP l eventually periodic in {hits}/{total} drives; "
                   f"l|Z eventually periodic in {lZ_hits}/{lZ_total}; moving-edge violations {evtot}; "
                   f"periodic single columns among -1..-8: {percol}; "
                   f"longest shift-agreement run over drives min/median/max = {min(runs)}/{sorted(runs)[len(runs)//2]}/{max(runs)} "
                   f"(random null log2(T*Q) = {math.log2(T*Q):.1f}) [{time.time()-wall:.0f}s elapsed]")
        tally[tag] = (hits, total, evtot, percol)
        print("\n".join(out)); out.clear()

    # ---- Part 1: periods 7 and 8, prefix 0, T = 2^15
    T7 = 1 << 15; Q7 = 512
    hits = 0; total = 0; evtot = 0; runs = []; percol = 0
    for w in periodic_words(7, 8):
        c = build_drive(w, [], T7)
        r = analyse_drive(f"P78 word {''.join(map(str, w))} prefix_len=0", 0, c, T7, Q7, ncols, out)
        total += 1; hits += r['ep_l'] is not None; evtot += r['ev']; runs.append(r['run']); percol += len(r['per_cols'])
    out.append(f"SUMMARY P78 rule30 T={T7} Q={Q7}: LHP l eventually periodic in {hits}/{total} drives (primitive words of period 7 and 8); "
               f"moving-edge violations {evtot}; periodic single columns {percol}; run min/median/max = {min(runs)}/{sorted(runs)[len(runs)//2]}/{max(runs)} "
               f"(null {math.log2(T7*Q7):.1f}) [{time.time()-wall:.0f}s]")
    tally['P78'] = (hits, total, evtot, percol)
    print("\n".join(out)); out.clear()

    # ---- Part 2: random nonzero finite y (support in x <= -1), periods 1..4, T = 2^15
    Ty = 1 << 15; Qy = 512
    rng = random.Random(2026)
    hits = 0; total = 0; evtot = 0; runs = []; percol = 0
    for w in periodic_words(1, 4):
        for seed in range(4):
            width = rng.randint(1, 24)
            y = 0
            while y == 0:
                y = sum(rng.getrandbits(1) << i for i in range(1, width + 1))
            c = [w[t % len(w)] for t in range(Ty + 2)]  # c_0 may be 0 here: y is the nonzero seed
            r = analyse_drive(f"RANDY word {''.join(map(str, w))} y=0x{y:x}", y, c, Ty, Qy, ncols, out)
            total += 1; hits += r['ep_l'] is not None; evtot += r['ev']; runs.append(r['run']); percol += len(r['per_cols'])
    out.append(f"SUMMARY RANDY rule30 T={Ty} Q={Qy}: LHP l eventually periodic in {hits}/{total} drives (random y, words of period 1..4); "
               f"moving-edge violations {evtot}; periodic single columns {percol}; run min/median/max = {min(runs)}/{sorted(runs)[len(runs)//2]}/{max(runs)} "
               f"(null {math.log2(Ty*Qy):.1f}) [{time.time()-wall:.0f}s]")
    tally['RANDY'] = (hits, total, evtot, percol)
    print("\n".join(out)); out.clear()

    # ---- Part 3: Rule 90 control (obstruction B): driven LHP with c = 1 0^inf and c = (10)^inf
    T9 = 1 << 15
    c0 = [1] + [0] * (T9 + 2)
    cols, ev = driven_lhp_y(0, c0, T9, 3, step90_mirror)
    l = cols[1]
    ones = np.flatnonzero(l)
    expect = [(1 << j) - 1 for j in range(1, 16)]
    out.append(f"RULE90 c=1 0^inf: l ones at t = {ones[:14].tolist()} expected 2^j-1: {expect[:14]} match={ones.tolist()==[e for e in expect if e <= T9]} "
               f"eventual_period={eventual_period_np(l, 512)} edge violations={ev}")
    c01 = build_drive([0, 1], [], T9)
    r = analyse_drive("RULE90 c=1(01)^inf", 0, c01, T9, 512, ncols, out, step=step90_mirror)
    c011 = build_drive([0, 1, 1], [], T9)
    r = analyse_drive("RULE90 c=(011)^inf", 0, c011, T9, 512, ncols, out, step=step90_mirror)
    print("\n".join(out)); out.clear()

    # ---- Part 4: deep runs, T = 2^20, Q = 4096, four drives
    hits = 0; total = 0; evtot = 0; runs = []
    for w in ([0], [0, 1], [0, 0, 1], [0, 1, 1]):
        c = build_drive(w, [], T_deep)
        r = analyse_drive(f"DEEP word {''.join(map(str, w))} prefix_len=0", 0, c, T_deep, Q_deep, 2, out, deep=True)
        total += 1; hits += r['ep_l'] is not None; evtot += r['ev']; runs.append(r['run'])
        print("\n".join(out)); out.clear()
    out.append(f"SUMMARY DEEP rule30 T={T_deep} Q={Q_deep}: LHP l eventually periodic in {hits}/{total} drives; moving-edge violations {evtot}; "
               f"run min/max = {min(runs)}/{max(runs)} (null {math.log2(T_deep*Q_deep):.1f}) [{time.time()-wall:.0f}s]")
    tally['DEEP'] = (hits, total, evtot, 0)
    tot_hits = sum(v[0] for v in tally.values()); tot = sum(v[1] for v in tally.values())
    tot_ev = sum(v[2] for v in tally.values())
    out.append(f"FINAL: l eventually periodic in {tot_hits}/{tot} driven left half-planes; moving-edge violations {tot_ev}; "
               f"verdict {'KILLED' if tot_hits or tot_ev else 'HOLDS'} [{time.time()-wall:.0f}s total]")
    print("\n".join(out))


if __name__ == '__main__':
    main()
