# NEGATIVE — no sequence-independent rung-to-rung induction exists at any level `n` (Theorem N, proved witness family `G_n = sum_j x^(2^(n j))`); row 46 stays OPEN and the missing lemma is unchanged and is Lemma L's HEIGHT half, "if `a` is 2-automatic with `k` states then `F` admits an Ore relation of height `<= poly(k)`" (the order half, order `<= m`, is already proved).

Row 46 stays **OPEN**. This document does not close it. It retires one named
sub-route inside it and localizes the remaining obligation.

Scripts and outputs in this directory:
`ore_uniformity.py`, `run_ore_uniformity.txt` (all checks pass, exit 0).
Run with `uv run python ore_uniformity.py` from this directory.

---

## 0. What was asked and what fired

Row 46 records a ladder `S(0) <= S(1) <= ...` with `S(0) <=> P1` exactly and
`AND_n S(n) <=>` non-2-automaticity of A051023 (Christol). Each rung is
one-sidedly provable by one finite GF(2) rank computation. The target was a
**uniform** argument over `n`: an inductive relation between `S(n)` and
`S(n+1)`, a rank recurrence, or a proof that the ladder's one-sided provability
is uniform — or a precise proof that no such uniformity exists by this route.

The kill condition that fired is the last one, in its strongest available form:

> **KILL — no sequence-independent rung-to-rung induction exists, at any level.**
> For every `n >= 1` there is an explicit power series over `F_2` whose ladder
> truth set is exactly `{0, ..., n-1}`. So an implication `S(n) => S(n+1)`
> proved from the ladder axioms alone (i.e. valid for every series) is false at
> every level `n`. Any uniform argument must consume a property of A051023
> itself that is not visible in the rungs.

Two theorems below. **N** is the kill. **U** is the exchange rate that says how
much of the ladder finite rank data can ever reach; it is Theorem O of
`overnight/RESULTS-automaticity.md` transported into the ladder's `(n,d)`
coordinates, not a new obstruction.

---

## 1. Theorem N — the witness family

**Definition.** For `n >= 1` let

```
G_n(x) := sum_{j >= 0} x^(2^(n*j))   in F_2[[x]].
```

**Theorem N.** `G_n` admits an Ore relation of order exactly `n`, at height 1.
Consequently `S(m)` is TRUE for `G_n` for every `m < n` and FALSE for every
`m >= n`.

*Upper bound (verified by machine).* Over `F_2` squaring doubles exponents, so
`G_n^(2^n)` has support `{2^(n*(j+1))}` and

```
x + G_n(x) + G_n(x^(2^n)) = 0,
```

i.e. `P_{-1} = x`, `P_0 = 1`, `P_n = 1`, height 1. Verified as an exact
identity on supports for `n = 1..8` out to exponent `2^2048`
(`check_theorem_n`); the sparse representation makes this exact, not sampled.

*Lower bound (proved here on paper, deliberately NOT computed).* Suppose
`Q_{-1} + sum_{i=0}^{k} Q_i G_n(x^(2^i)) = 0` with `k < n`, all `deg Q_i <= d`,
not all zero.

> **Separation lemma.** The support of `G_n(x^(2^i))` is `{2^(i + n*j) : j >= 0}`.
> For `0 <= i <= k < n` the exponents `e = i + n*j` are pairwise distinct across
> all pairs `(i,j)`, because `i` is the residue of `e` mod `n` and `i < n`.
> Multiplying by `Q_i` (degree `<= d`) smears the support point `2^e` into the
> block `[2^e, 2^e + d]`. If `2^e > d` then for any larger exponent `e' > e` we
> have `2^(e') >= 2^(e+1) = 2^e + 2^e > 2^e + d`, so the blocks of `e` and `e'`
> are disjoint. Hence all blocks with `2^e > d` are pairwise disjoint, and all
> of them lie strictly above `d >= deg Q_{-1}`.

Pick any `i` with `Q_i != 0`, and pick `j` large enough that `2^(i + n*j) > d`.
Put `E := 2^(i + n*j) + deg Q_i`. Then `E` lies in the block of the exponent
`e = i + n*j` and in no other block, and `E > d` so `Q_{-1}` cannot reach it.
So the coefficient of `x^E` on the left-hand side is exactly the leading
coefficient of `Q_i`, which is 1 in `F_2` and has nothing to cancel against.
Contradiction. Hence every `Q_i = 0`, then `Q_{-1} = 0`. Minimal order is
exactly `n`. Both hypotheses the argument rests on — pairwise disjointness of
the raw Frobenius supports, and pairwise disjointness of the `d`-smeared blocks
past the threshold `2^e > d` — are checked by machine for `n = 1..8` at
`d = 100` (`check_theorem_n`), together with a disconfirming control: the same
separation check with the threshold `2^e > d` removed returns False, so the
check is not vacuous.

*Why the lower bound is not computed.* The nullity instrument is one-sided:
nullity `> 0` never proves that a relation exists, only that none is excluded.
On a lacunary series almost every truncation row is identically zero, so
nullity `0` is unreachable at feasible `N` for anything but tiny `d`, and a
computed nullity there would be an instrument-resolution artifact read as
mathematics. The bound is analytic and needs no computation.

**Relation to what row 46 already records.** `RESULTS-automaticity.md` lines
33-36 already state ladder strictness at rung 0, with Thue-Morse as the
witness that `S(0)` does not imply `S(1)`. Theorem N is the **upgrade of that
single-level fact to every level**, with a proved witness family rather than
one example. `G_1 = sum_j x^(2^j)` (characteristic function of the powers of 2,
satisfying `x + G_1 + G_1^2 = 0`) is a second, independent rung-0 witness
alongside Thue-Morse. Strictness at rung 0 is not claimed as new here.

**Consequence, stated precisely.** Let `n*(F) := min{n : F admits an Ore
relation of order n}` (`= infinity` if none). The ladder truth set of any `F`
is the initial segment `{0, ..., n*(F)-1}` — monotone, no gaps, since an
order-`n` relation is an order-`(n+1)` relation with `P_{n+1} = 0`. Theorem N
shows every FINITE value `n* = 1, 2, 3, ...` is realized by an explicit series,
and `n* = 0` is realized by any rational series, e.g. `F = 1/(1+x)` or the
Rule 90 lone-seed centre column (caught at `(0,0)` in the control below).
Whether `n* = infinity` is realized is not asserted here: that is exactly the
statement `AND_n S(n)`, i.e. transcendence over `F_2(x)`, which holds for
non-2-automatic series but is not exhibited by this document. Therefore the map `S(n) -> S(n+1)` carries no
sequence-independent content whatsoever: knowing that a series clears rungs
`0..n` constrains rung `n+1` not at all. A uniformity proof cannot be an
induction on the rungs.

---

## 2. Theorem U — the ladder's exchange rate

The truncated system at order `n`, height `d`, on coefficient rows
`x^0 .. x^(N-1)`, has exactly `(n+2)(d+1)` unknowns and `N` equations.

**Theorem U (counting form).** `nullity(n,d,N) >= max(0, (n+2)(d+1) - N)`.
Hence an `S(n,d)` certificate requires `N >= (n+2)(d+1)` terms of `a`; the
region of the ladder reachable from `N` terms is the hyperbolic set
`{(n,d) : (n+2)(d+1) <= N}`.

**Theorem U (explicit-witness form).** For `d >= N-1`, the pair
`P_{-1} = sum_{m<N} a(m) x^m`, `P_0 = 1` is an exact nonzero solution of the
truncation for **every** sequence `a`. So no finite `N` certifies `S(n)` — the
unbounded-height statement — for even one `n`.

Verified over a grid on A051023 and on the Thue-Morse control, including cases
where the counting bound is tight and cases where it is slack
(`run_ore_uniformity.txt`, sections 2 and 3). The named witness is verified to
be in the nullspace in the instrument's own column algebra, residual 0, at
`N = 17, 33, 65`.

**Exchange rate at the register's `N = 32000`.** Every number in this table
bounds a complexity function on a finite prefix and can never establish the
infinite statement (Theorem O / obstruction H):

| order `n` | max certifiable height `d` from 32000 terms |
|---:|---:|
| 0 | 15999 |
| 1 | 10665 |
| 2 | 7999 |
| 3 | 6399 |
| 6 | 3999 |
| 12 | 2284 |
| 100 | 312 |
| 1000 | 30 |

Max order certifiable at height `>= 1`: `n = 15998`. The certificates actually
computed in `RESULTS-automaticity.md` (order `<= 12`, heights to 570) sit at
`(12+2)*571 = 7994 <= 32000`, comfortably inside this region — the bound is not
binding on past work, it bounds future work. Again: this is finite-prefix data
bounding a complexity function, never the infinite statement.

**What U is and is not.** It is Theorem O localized to the ladder's grid, not
an independent obstruction, and it is soft: a linear data cost, weaker than
Theorem O's `N/8` kernel rate. Its role is only to make explicit that the
ladder route's finite half is bounded in exactly the same way everything else
computed from a prefix is bounded.

---

## 3. Rule 90 control, and why the filter does not apply in its usual direction

Run in `run_ore_uniformity.txt` section 4, same code path as the target:

| series | `(n,d)` | nullity | reading |
|---|---|---:|---|
| Rule 90 centre | (0,0) | 1 | relation exists, `n* = 0` |
| Rule 90 centre | (1,5) | 12 | relation exists |
| Rule 30 centre | (0,50) | 0 | `S(0,50)` certified |
| Rule 30 centre | (1,20) | 0 | `S(1,20)` certified |
| Rule 30 centre | (2,20) | 0 | `S(2,20)` certified |
| Rule 30 centre | (3,20) | 0 | `S(3,20)` certified |

Instrument calibration in section 0: Thue-Morse `(1,2)` nullity 0 (tight, not
permissive), `(1,3)` nullity 1 (known witness recovered), Rule 90 `(0,0)`
caught. These reproduce the row-46 table on independent code and are stated
here as continuity, not as new results. Each of these zeros bounds a
complexity function on a finite prefix and can never establish the infinite
statement.

**The filter inverts here.** Theorems N and U are negative statements about a
certification *route*, not positive statements about Rule 30, and they hold
verbatim for Rule 90 — as they must. It would be wrong to write "this passes
the Rule 90 filter"; the filter tests arguments that would prove P1, and this
document proves no part of P1.

---

## 4. Where Lemma L's difficulty actually lives, after this

The conversion in `RESULTS-automaticity.md` is: if `a` is 2-automatic and `m`
is the GF(2) dimension of the span of its 2-kernel, then with
`G(x) = A(x) G(x^2)`, `A` an `m x m` matrix over `F_2[x]` of entry degree
`<= 1`, one gets `G(x^(2^i)) = B_i G(x)` with

```
B_i = (A^-1)^(2^(i-1)) * ... * (A^-1)^(2) * (A^-1),
```

and `m+1` of the row vectors `e_1^T B_i` are `F_2(x)`-dependent — giving order
`<= m`, already linear in the kernel dimension and already fine. The
exponential in the proved bound `height <= m * 2^(2m)` comes **entirely** from
degree growth in that iterated Frobenius product: `deg B_i` grows like
`2^i * deg(A^-1)`.

So the decisive question behind Lemma L is sharpened to:

> Does there exist a `k`-state 2-automatic sequence whose minimal Ore height is
> `2^(Theta(k))`, or is the true height bound `poly(k)`?

This is a question about the class of automatic sequences, a finite search at
each `k` — **not** a question about Rule 30 or about any prefix of A051023.
Obstruction H therefore does not apply to it. It is the correct next target for
row 46 and is left uncomputed here on purpose: computing it is a different
experiment with its own pre-registration.

---

## 5. What a reader must not over-read

1. **Row 46 is not closed.** One sub-route inside it is. Lemma L's height half
   is untouched.
2. **Nothing here bears on P1.** Theorem N is about arbitrary power series;
   Theorem U is a data-cost bound. Neither excludes any behaviour of A051023.
3. **Theorem N's lower bound is a paper proof, not a computation.** The machine
   checks only the order-`n` relation and the support-disjointness hypothesis.
4. **Every rank number quoted here is finite-prefix data.** It bounds a
   complexity function on that prefix and can never establish the infinite
   statement (Theorem O: for every `N` the sequence agreeing with `a` on
   `[0,N)` and zero thereafter is eventually periodic, hence 2-automatic).
5. **The order-0 certificates remain elementary.** As `RESULTS-automaticity.md`
   already states, an order-0 nullity-0 certificate is equivalent to a direct
   finite periodicity check; the new content of the arm was and remains the
   order `>= 1` rungs.
6. **Ladder strictness at rung 0 is prior work in this repo**
   (`RESULTS-automaticity.md` lines 33-36, Thue-Morse). What is new here is the
   extension to every level with a proved witness family.
