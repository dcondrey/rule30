# Brief for the 2026-09-02 ultracode attack on Rule 30 Problem 1

This is the shortest correct statement of where the attack stands.
Everything in it is verified by code that can be run.

## 0. Working rules

- Kernel modules for this thread: `psi_kernel.py`, `rw_margin.py`,
  `binary_wedge_high_elimination.py`, `dyadic_periodicity_analyzer.py`,
  `rank_zero_separator.py`, importable from
  `experiments/rule30/p1-period2-invariant`.
- Every numerical claim must name the script and log that produced it.
- Do not spend a test confirming something this brief already states as
  verified. Test what is OPEN.
- Do not rename and retry anything in section 6. An idea that is a
  relabeling of a killed mechanism should say so and stop.

## 1. The problem and the target chain

**Problem 1 (Wolfram, 2019 prize).** The centre column `c_t` of Rule 30 from a
single black cell is not eventually periodic.

The live attack is period-specific. Constant tails are excluded (proved). The
next case is period two, and it has been reduced along this proved chain
(`PROOF-STATE-CAPSULE.md` section 1):

```text
(PT2) Tr_0(y) != Tr_0(F^2(y)) for every nonzero finite y     [period-two exclusion]
  <= (SEP)  O_c intersect I(HC_omega) = empty, c in {2,3}
  <= (DLP)  <=> (RW)   the rotated wedge, stated in section 3 below
  <= (BWH+) the binary wedge horizon                          [RETIRED today, see section 5]
```

`A <= B` means `B` implies `A`. So proving `(RW)` proves `(PT2)`. Proving
`(PT2)` does NOT prove Problem 1; it excludes one period.

## 2. The four-state kernel, in coordinates that decouple

Cells are four-state, `T in {0,1,2,3}`, with bits `H = T>>1` (high) and
`Lo = T&1` (low). Define the **defect** `E = 1 + H + Lo mod 2`. The binary
symbols `{1,2}` are exactly `E = 0`; the equality symbols `{0,3}` are `E = 1`.

The triangle. Endpoint symbols `e_0, e_1, ..., e_{L-1}` in `{0..3}`. Cells
`T[u][d]` for column `u` and depth `d in [-u-1, u]`:

```text
    T[u][-u-1] = e_u
    T[u][-u]   = e_u XOR 3
    T[u][d]    = phi(T[u-1][d-1], T[u][d-1])      for d > -u
```

where `phi` is the local rule (`CONE[l][r]` in `psi_kernel.py`). `phi` is a
bijection in its right argument for every fixed left argument.

**The rule decouples** (exhaustive over all 16 argument pairs):

```text
    H(phi(l, r)) = H(r) + 1 + [l == 0]
    E(phi(l, r)) = E(r) + H(r) * [Lo(l) == 0]
```

**Column integrals** (verified on 134,642 cells): with the quotient letters
`a = [T == 0]`, `b = [Lo(T) == 0]` of column `u-1`,

```text
    H_u(d) = H(e_u) + (d + u + 1) + #{d' in [-u, d) : a(T[u-1][d']) = 1}
    E_u(d) =                        #{d' in [-u, d) : H_u(d') = 1 and b(T[u-1][d']) = 1}
```

**The column map is a fixed 4-state Moore transducer** (verified on 17,410
columns): state `(h, F) = (H_u(d), E_u(d))`, reading column `u-1`'s quotient
letters `(a, b)` from `d = -u` upward, starting at `(1 - H(e_u), 0)`:

```text
    step(h, F, a, b) = (h XOR 1 XOR a,  F XOR (h AND b))
```

The cell `T[u][d]` is `2h + (1 + h + F mod 2)`, i.e. the column IS the state
trajectory. The three letters `(0,0)`, `(0,1)`, `(1,1)` induce the maps
translation `h -> h+1`, composite, and shear `F -> F+h`; they generate the
group of order 8 (the affine `D8` of the capsule).

The quotient is 4-to-3: cells `1` and `3` both map to `(0,0)`. Column `u`'s
full four-state content is recovered from column `u-1`'s three-letter quotient
plus the one bit `H(e_u)`.

## 3. The target `(RW)`, in three equivalent forms

**Word form** (`RESULTS-DLP-ROTATED-WEDGE.md`). There are no `n >= 1`,
`r in {0,1,2}`, `c in {2,3}` and binary `f in {1,2}^(2n+r+2)` such that

1. `f[n:]` is hard-core (no `11`), including its junction with `f[n-1]`;
2. `P^n(I(f)) = c^(n+r+2)`, i.e. `T[u][n] = c` for `u = n, ..., 2n+r+1`;
3. `f[-3:-1] = 12`.

**Orbit form** (verified today, 131,580 checks). For `u >= n`, the symbol
`e_u in {1,2}` is FORCED by column `u-1` through the `H` constraint
`H(T[u][n]) = 1`, and then

```text
    E(T[u][n]) = Phi(col_{u-1})
```

where `Phi` is the quadratic form over column `u-1` on the window
`d in [-u, n-1]` (edge symbol `e_{u-1}` sits at `d = -u`), written with the
indicators `a' = [T != 0]` and `b = [Lo(T) == 0]`:

```text
    alpha' = sum a'_d,  beta = sum b_d,  gamma' = sum_{d' < d} a'_{d'} b_d   (all mod 2)
    Phi = beta * (1 + alpha') + gamma'
```

**ERRATUM (corrected 2026-09-02, after this thread began).**  An earlier
version of this paragraph wrote `a = [T == 0]` here.  That is the indicator
in the Moore STEP (`h -> h XOR 1 XOR a`), and it is correct there; in `Phi` the
indicator is `a' = [T != 0] = 1 + a`.  The two forms are related by
`alpha' = |window| + alpha` and `gamma' = sum_d (index of d) b_d + gamma`, and
only the primed form is verified (131,580 checks).  Equivalent set form, also
verified: with `Z` the zero cells, `W2` the cells equal to `2`, `N` the nonzero
cells of the window and `m = n + u` its length,

```text
    H(e_u) = 1 + (n + u + 1) + |Z|                                   (H-forcing)
    Phi    = (|Z| + |W2|) (1 + m + |Z|) + #{(x, y) : x < y, x in N, y in Z or W2}
```

If you derived anything from the unprimed form, rederive it.

So `(RW)` says: the deterministic forced map `M*` on columns, started from the
`2^n` binary prefixes `W`, never produces `n+r+2` consecutive columns in the
hit set `G_c = {col : Phi(col) = E(c)}` while keeping the forced symbols
hard-core and ending in `12a`.

**Diagonal form** (verified today, `n = 1..4`). The set
`{g in {0..3}^L : P^n(I(g)) = c^(L-n)}` has exactly `4^n` elements, and the
main diagonal `(T[0][0], ..., T[n-1][n-1]) in {0..3}^n` is a bijective
parameter for it. `(RW)` asks whether any of those `4^n` words has all `L`
edge symbols binary (`E = 0`) with hard-core suffix and `12a` ending: `2n`
free bits against `2n + r + 2` constraints.

## 4. What is measured about `(RW)` (complete search, not sampled)

`rw_margin.py`, `n = 7..17`, hardest case `r = 0`:

| n | deepest run of `c` cells | need | slack |
|---|---|---|---|
| 9 | 8 | 11 | 3 |
| 12 | 9 | 14 | 5 |
| 15 | 9 | 17 | 8 |
| 17 | 11 | 19 | 8 |

`deepest / n` sits at `0.6 to 0.75` with no upward trend. Surviving-prefix
counts `N_k` decay at `1.35 +/- 0.15` bits per column (predicted `1.415`: one
bit for the `E` constraint, `log2(4/3)` for the hard-core kill).

**Sufficient rate target.** `(RW-alpha)`: there are `alpha < 1`, `C` with no
admissible run longer than `alpha * n + C` for all `n`. This implies `(RW)`
for large `n`; the small `n` are decidable by the search.

**A naive counting bound is FALSE.** `N_k <= 2^(n-k)` fails at
`(n, c, k) = (3,3,1), (4,2,2), (7,3,4)` with ratio up to 4. Any counting
lemma must carry a constant: `N_k <= C * 2^(n - lambda k)` with `lambda >= 1`
suffices for `(RW)` at large `n`.

## 5. What was retired today, and why

`(BWH+)` (constant `Psi_n(W)` for arbitrary binary `W`, only the high bit
pinned) is the wrong target:

- `Delta_j = Psi_j + Psi_{j+1}` has FULL algebraic degree `n` in the source
  bits at every `n` from 4 to 15. No bounded-arity seam law exists; the
  complete-state recursion necessarily fans out. This is the capsule's own
  pre-authorised trigger to fall back to `(RW)`.
- Its slack is 1: at `n = 15`, 18 sources are constant on `Psi_0..Psi_15` and
  flip only at `Psi_16`. All 18 share the suffix `211212112`. They die
  simultaneously. The shared cause is NOT identified.
- Its survivor counts are at the independence null (`R_k = 1.00 +/- 0.05`)
  then cluster to `R_k = 18`. Nothing about `(BWH+)`'s truth can be read from
  counting.

`(RW)` differs from `(BWH+)` by pinning the WHOLE Moore state `(h, F)` at depth
`n` rather than only `h`, and by the hard-core suffix. Those two facts are the
entire difference between slack 1 and slack `0.35n`.

## 6. Killed mechanisms. Do not rename and retry.

From `PROOF-STATE-CAPSULE.md` section 5, each with an exact counterexample:

| Mechanism | Exact obstruction |
|---|---|
| Fixed-radius additive energy / potential | Farkas contradictions for localities 1..4; radius-seven negative cycles |
| Fixed finite quotient of the frontier | Same summary with different legal successors; carry actions are permutations |
| Bare holonomy-defect word | Identical profiles with different next rows at length 8; two-ended repair fails at 13 |
| Static formula / DFA rank contraction | Survivor DFA size grows as `4^(h+1)+1` through the checked range |
| One backward source defect | Single-coordinate relaxations remain UNSAT; the obstruction is branched/global |
| Pointwise scale derivative / matching | Exact failure first appears at length 21 |
| Sharp bound `M_c(n) <= n` | `M_3(15) = 16` |
| Larger bounded SAT/GA tables | Falsify candidates but cannot supply the all-length quantifier |
| Bounded-arity seam law for `Delta` | Full algebraic degree `n` (today) |

From `PATH.md` section 7.3, the eight standing obstructions for Problem 1 as a
whole: **A** the `O(log t)` wall (trace-anchored analysis reaches
`~2.4 log2 t` into a diagram whose target is at distance `Theta(t)`); **B**
the Rule 90 filter (any argument that also applies to Rule 90 proves nothing,
since Rule 90's lone-seed centre column IS eventually periodic); **C**
single-column blindness; **D** the missing composition law (naming a lemma
instead of deriving it); **E** the measure-zero single-orbit gap; **F** the
free boundary of a fixed-depth strip; **G** arbitrary-input measures versus a
single fixed point; **H** finite data cannot establish an infinite statement.

A proposal must say, for each of A through H, either "not applicable because
..." or "evaded because ...".

## 7. What a useful deliverable looks like

A **lemma** is useful only if all four hold:

1. It is stated precisely in the language of section 2 or 3 (or another exact
   language you define completely).
2. You say which of `(RW-alpha)`, `(RW)`, `(SEP)`, `(PT2)`, P1 it implies, and
   the implication is either one of the proved arrows in section 1 or you
   prove it.
3. It has a **kill test**: a finite computation on the existing kernel that
   would refute it if it is false, and which can plausibly fire. State the
   `n` range and what a failure looks like.
4. It is not in section 6, and you say which section-6 row it is closest to
   and exactly why it differs.

A **proof** is useful only if every step is one of: a verified identity from
section 2; a proved arrow from section 1; a finite exhaustive check with a
script and log; or a derivation you write out in full. "Clearly", "it is easy
to see", and "by a standard argument" are each a gap and must be listed as one.

An honest negative (a lemma killed by its own kill test, with the exact
counterexample) is a real result and is recorded.
