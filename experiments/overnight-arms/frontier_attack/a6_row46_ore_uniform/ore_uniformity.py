"""Row 46: is the Ore-relation ladder S(0) <= S(1) <= ... uniform in n?

NEGATIVE instrument. This script does NOT try to certify more rungs (row 17 already
fired both its kills; more rank data is not a contribution). It verifies the two
finite, checkable halves of a negative answer:

  THEOREM N (no sequence-independent rung-to-rung induction).
      G_n(x) := sum_{j>=0} x^(2^(n*j))  in F_2[[x]]   (n >= 1)
      satisfies  G_n^(2^n) = G_n + x,  an Ore relation of order exactly n, height 1.
      Minimal order is exactly n (support/gap proof, in the .md; analytic, not computed).
      Hence for every n there is a series whose ladder truth set is exactly {0,...,n-1},
      so no implication "S(n) => S(n+1)" holds for all series, at any level n.
      Here we verify only the POSITIVE half: the order-n relation, by exact series
      arithmetic mod x^M.  Also verified: G_n admits no Ore relation of order < n
      is NOT checked numerically -- the nullity instrument is one-sided and on a
      lacunary series its rows are nearly all zero, so a null result there would be
      an instrument-resolution artifact, not evidence.  The lower bound is proved on
      paper instead.

  THEOREM U (Theorem O transported into ladder coordinates).
      The truncated system on rows x^0..x^(N-1) at order n, height d has exactly
      (n+2)(d+1) unknowns and N equations, so
          nullity(n,d,N) >= max(0, (n+2)(d+1) - N),
      and in particular no S(n,d) certificate is possible unless (n+2)(d+1) <= N.
      Explicit-witness form: for d >= N-1 the pair P_{-1} = sum_{m<N} a(m) x^m,
      P_0 = 1 is an exact nonzero solution of every truncation, so no finite N ever
      certifies S(n) at unbounded height.

Every number this script prints bounds a complexity function on a finite prefix and
can never establish the infinite statement (obstruction H / Theorem O).

Run: uv run python ore_uniformity.py
"""

from __future__ import annotations

import logging

log = logging.getLogger(__name__)


# ---------------------------------------------------------------- sequences
def rule_column(rule: str, n: int) -> list[int]:
    """Lone-seed centre column of an elementary CA, bit-parallel. Copied from
    experiments/overnight-arms/automaticity/ore_check.py (unmodified logic)."""
    row = 1
    out = []
    for t in range(n):
        out.append((row >> t) & 1)
        row = (row << 2) ^ ((row << 1) | row) if rule == "30" else (row << 2) ^ row
    return out


def thue_morse(n: int) -> list[int]:
    return [bin(t).count("1") & 1 for t in range(n)]


def lacunary_support(n: int, log2_bound: int) -> set[int]:
    """Exponent support of G_n = sum_{j>=0} x^(2^(n*j)), for exponents < 2^log2_bound.

    Returned as the set of exponents {2^(n*j)} rather than a coefficient list: the
    series is lacunary, so the sparse representation is exact and lets the identity
    be checked to exponent 2^log2_bound instead of a few million.
    """
    out = set()
    j = 0
    while n * j < log2_bound:
        out.add(1 << (n * j))
        j += 1
    return out


# ---------------------------------------------------------------- Ore instrument
def nullity(seq: list[int], n_ord: int, d: int, N: int) -> int:
    """dim of nullspace of the truncated Ore system over F_2, via bitset elimination.

    Unknowns: P_{-1}[0..d] then P_i[0..d] for i=0..n_ord  -> (n_ord+2)*(d+1) columns.
    Rows: coefficients of x^0..x^(N-1).
    Copied from ore_check.py; identical construction, so results are comparable.
    """
    cols = []
    for j in range(d + 1):
        cols.append(1 << j if j < N else 0)
    for i in range(n_ord + 1):
        step = 1 << i
        for j in range(d + 1):
            v = 0
            for m in range(j, N):
                r = m - j
                if r % step == 0:
                    idx = r // step
                    if idx < len(seq) and seq[idx]:
                        v |= 1 << m
            cols.append(v)
    pivots: list[int] = []
    rank = 0
    for c in cols:
        cur = c
        for p in pivots:
            low = p & -p
            if cur & low:
                cur ^= p
        if cur:
            pivots.append(cur)
            rank += 1
    return len(cols) - rank


# ---------------------------------------------------------------- checks
def check_calibration() -> list[str]:
    """The instrument must FIND relations where relations are known to exist."""
    fails = []
    tm = thue_morse(4000)
    n2 = nullity(tm, 1, 2, 4 * 2 * 3 + 60)
    n3 = nullity(tm, 1, 3, 4 * 2 * 4 + 60)
    log.info("calib Thue-Morse (n=1,d=2): nullity=%d  (expect 0: instrument is tight)", n2)
    log.info("calib Thue-Morse (n=1,d=3): nullity=%d  (expect >0: known witness)", n3)
    if n2 != 0:
        fails.append("Thue-Morse (1,2) should have nullity 0")
    if n3 == 0:
        fails.append("Thue-Morse (1,3) relation not found")
    r90 = rule_column("90", 4000)
    n90 = nullity(r90, 0, 0, 200)
    log.info("calib Rule 90 centre  (n=0,d=0): nullity=%d  (expect >0: caught at order 0)", n90)
    if n90 == 0:
        fails.append("Rule 90 not caught at order 0")
    return fails


def smeared_blocks_disjoint(n: int, k: int, d: int, j_max: int) -> tuple[bool, int]:
    """Separation lemma check: the blocks [2^(i+n*j), 2^(i+n*j)+d] for 0<=i<=k<n,
    0<=j<=j_max, restricted to those with 2^(i+n*j) > d, are pairwise disjoint and
    all lie strictly above d.

    This is the hypothesis the paper lower bound actually uses (disjointness AFTER
    smearing by deg Q_i <= d), not the weaker raw-support disjointness.
    Returns (ok, number of blocks tested).
    """
    blocks = []
    for i in range(k + 1):
        for j in range(j_max + 1):
            e = i + n * j
            start = 1 << e
            if start > d:
                blocks.append((start, start + d))
    blocks.sort()
    ok = all(blocks[t][1] < blocks[t + 1][0] for t in range(len(blocks) - 1))
    ok = ok and all(s > d for s, _ in blocks)
    return ok, len(blocks)


def check_theorem_n(max_n: int = 8, log2_bound: int = 2048) -> list[str]:
    """Positive half of Theorem N, by exact sparse series arithmetic mod x^(2^B).

    (i) Verify x + G_n + G_n^(2^n) == 0 mod x^(2^B): the order-n, height-1 Ore
        relation P_{-1}=x, P_0=1, P_n=1.  Over F_2 a series squares by doubling
        exponents, so G_n^(2^n) has support {2^(n*(j+1))}.
    (ii) Verify the hypothesis the paper lower-bound argument uses: the supports of
        G_n^(2^i) for i=0..n-1 are pairwise disjoint (exponents 2^(i+n*j), distinct
        residues i mod n), so a putative relation of order < n cannot cross-cancel.
    The order-< n LOWER bound itself is proved on paper, not here: the nullity
    instrument is one-sided and on a lacunary series almost every truncation row is
    zero, so a computed nullity there would be an instrument artifact.
    """
    fails = []
    for n in range(1, max_n + 1):
        g = lacunary_support(n, log2_bound)
        frob = {e << n for e in g if e.bit_length() - 1 + n < log2_bound}
        # x + G + G^(2^n): symmetric difference of supports, {1} for x
        lhs = ({1} ^ g) ^ frob
        # truncate: only exponents below 2^log2_bound are asserted
        lhs = {e for e in lhs if e.bit_length() - 1 < log2_bound}
        supports = [{e << i for e in g if e.bit_length() - 1 + i < log2_bound}
                    for i in range(n)]
        disjoint = all(
            not (supports[i] & supports[j]) for i in range(n) for j in range(i + 1, n)
        )
        d_test = 100
        sep_ok, nblocks = smeared_blocks_disjoint(n, n - 1, d_test, j_max=40)
        log.info(
            "Theorem N  G_%d = sum_j x^(2^(%dj)):  x + G + G^(2^%d) has %d nonzero "
            "coefficients below x^(2^%d) (expect 0); Frobenius supports i=0..%d "
            "pairwise disjoint: %s; separation lemma at d=%d, %d blocks past the "
            "threshold 2^e > d pairwise disjoint and all above d: %s",
            n, n, n, len(lhs), log2_bound, n - 1, disjoint, d_test, nblocks, sep_ok,
        )
        if lhs:
            fails.append(f"G_{n} does not satisfy its order-{n} relation")
        if n > 1 and not disjoint:
            fails.append(f"G_{n} Frobenius supports not disjoint")
        if not sep_ok:
            fails.append(f"G_{n} separation lemma fails at d={d_test}")
    # Disconfirming control: the separation check must FAIL when the threshold
    # 2^e > d is dropped, otherwise it is vacuous and proves nothing.
    blocks = []
    for i in range(3):
        for j in range(6):
            s = 1 << (i + 3 * j)
            blocks.append((s, s + 100))
    blocks.sort()
    below_threshold_ok = all(blocks[t][1] < blocks[t + 1][0] for t in range(len(blocks) - 1))
    log.info(
        "Theorem N  disconfirming control: same check with the 2^e > d threshold "
        "REMOVED (n=3, d=100) -> disjoint: %s (expect False; a True here would mean "
        "the separation check is vacuous)", below_threshold_ok,
    )
    if below_threshold_ok:
        fails.append("separation check is vacuous: it passes without its threshold")
    return fails


def check_theorem_u(seq: list[int], label: str) -> list[str]:
    """Theorem U, both forms, on a grid.

    (a) counting form: nullity(n,d,N) >= max(0, (n+2)(d+1) - N), and > 0 whenever
        (n+2)(d+1) > N.
    (b) explicit-witness form: for d >= N-1, P_{-1} = truncation polynomial, P_0 = 1
        is an exact solution of the truncation -> nullity > 0.
    """
    fails = []
    grid = [
        (0, 6, 8), (0, 6, 14), (0, 6, 40),
        (1, 5, 12), (1, 5, 18), (1, 5, 60),
        (2, 4, 15), (2, 4, 20), (2, 4, 80),
        (3, 3, 16), (3, 3, 20), (3, 3, 90),
        (4, 2, 15), (4, 2, 18), (4, 2, 70),
    ]
    for n_ord, d, N in grid:
        unk = (n_ord + 2) * (d + 1)
        nl = nullity(seq, n_ord, d, N)
        bound = max(0, unk - N)
        ok = nl >= bound and (nl > 0 if unk > N else True)
        log.info(
            "Theorem U %s (n=%d,d=%d,N=%d): unknowns=%d rows=%d nullity=%d "
            "counting bound=%d  %s",
            label, n_ord, d, N, unk, N, nl, bound, "ok" if ok else "VIOLATED",
        )
        if not ok:
            fails.append(f"Theorem U counting form violated at ({n_ord},{d},{N}) on {label}")
    # (b) explicit witness
    for N in (17, 33, 65):
        d = N - 1
        nl = nullity(seq, 0, d, N)
        # verify the named witness directly in the same column algebra the instrument
        # uses: P_{-1}[j] = a(j) for j < N (its column is the single bit j), P_0 = 1
        # (its column is F truncated to N terms). Their XOR must be the zero vector.
        acc = 0
        for j in range(N):
            if seq[j]:
                acc ^= 1 << j
        f_trunc = 0
        for m in range(N):
            if seq[m]:
                f_trunc |= 1 << m
        residual = acc ^ f_trunc
        log.info(
            "Theorem U %s explicit witness (n=0,d=N-1=%d,N=%d): nullity=%d (expect >0); "
            "named witness P_{-1}=sum_{m<N} a(m)x^m, P_0=1 residual on rows [0,%d) = %d "
            "(expect 0)",
            label, d, N, nl, N, residual,
        )
        if nl == 0 or residual != 0:
            fails.append(f"Theorem U witness form violated at N={N} on {label}")
    return fails


def check_controls() -> list[str]:
    """Rule 90 / Rule 30 continuity control. Reproduces a subset of the row-46 table.

    NOTE: the Rule 90 filter does not apply in its usual direction to a negative
    theorem about a certification route -- Theorems N and U are statements about the
    ladder, not about Rule 30, and they hold for Rule 90 too. This control is run for
    continuity with the register, not as evidence for the theorems.
    """
    fails = []
    r90 = rule_column("90", 4000)
    r30 = rule_column("30", 40000)
    assert "".join(map(str, r30[:16])) == "1101110011000101", "ground-truth prefix mismatch"
    for n_ord, d in ((0, 0), (1, 5)):
        N = 4 * (n_ord + 2) * (d + 1) + 200
        nl = nullity(r90, n_ord, d, N)
        log.info("control Rule 90 (n=%d,d=%d,N=%d): nullity=%d %s",
                 n_ord, d, N, nl, "RELATION EXISTS -> n* = 0" if nl else "none")
        if nl == 0:
            fails.append(f"Rule 90 uncaught at ({n_ord},{d})")
    for n_ord, d in ((0, 50), (1, 20), (2, 20), (3, 20)):
        N = 4 * (n_ord + 2) * (d + 1) + 200
        nl = nullity(r30, n_ord, d, N)
        log.info("control Rule 30 (n=%d,d=%d,N=%d): nullity=%d %s",
                 n_ord, d, N, nl, "relation" if nl else "none -> S(n,d) certified")
        if nl != 0:
            fails.append(f"Rule 30 unexpected relation at ({n_ord},{d})")
    return fails


def frontier(N: int = 32000) -> None:
    """Theorem U exchange rate, printed as the certifiable region for the register's N."""
    log.info("Theorem U exchange rate at N=%d terms: certifiable region is "
             "{(n,d) : (n+2)(d+1) <= N}", N)
    for n_ord in (0, 1, 2, 3, 6, 12, 100, 1000):
        log.info("  order n=%5d -> max certifiable height d = %d", n_ord, N // (n_ord + 2) - 1)
    log.info("  max order certifiable at height >= 1: n = %d", N // 2 - 2)
    log.info("  This bounds a complexity function on a finite prefix and can never "
             "establish the infinite statement (Theorem O / obstruction H).")


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    fails: list[str] = []
    log.info("== 0. calibration (instrument must find known relations) ==")
    fails += check_calibration()
    log.info("")
    log.info("== 1. Theorem N: witness family, positive half, exact series arithmetic ==")
    fails += check_theorem_n()
    log.info("")
    log.info("== 2. Theorem U: counting + explicit-witness forms, on A051023 ==")
    r30 = rule_column("30", 40000)
    fails += check_theorem_u(r30, "Rule30")
    log.info("")
    log.info("== 3. Theorem U on the Thue-Morse control (must hold for any sequence) ==")
    fails += check_theorem_u(thue_morse(4000), "ThueMorse")
    log.info("")
    log.info("== 4. Rule 90 / Rule 30 continuity control ==")
    fails += check_controls()
    log.info("")
    log.info("== 5. exchange rate ==")
    frontier()
    log.info("")
    if fails:
        log.info("VERDICT: FAILURES (%d):", len(fails))
        for f in fails:
            log.info("  - %s", f)
        raise SystemExit(1)
    log.info("VERDICT: all checks passed. Scope: Theorem N's lower bound is proved on "
             "paper, not here; every table above is finite-prefix data and bounds a "
             "complexity function only.")


if __name__ == "__main__":
    main()
