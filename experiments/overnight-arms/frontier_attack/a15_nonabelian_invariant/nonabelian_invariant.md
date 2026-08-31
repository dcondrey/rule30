# Non-abelian transfer invariants of Rule 30: NEGATIVE. Step 0 survived at the class level (contra expectation), the search then FOUND 1,988 verified invariants rather than absence, and every one of them is killed individually — by the orbit-phase bound (<= 1.585 bits about the entire orbit, width- and monoid-independent) and by step 0 applied per survivor (ZERO column-0 disagreement at W >= 64). In every group cell the survivor set is exactly the coboundary space, proved by set equality. Rule 90's 567 invariants ARE column-sensitive, at the positive-control level, and are eventually constant: the filter fires as hard as it can.

Register row 53 / TRIAGE row 4's "group/monoid-valued" reading, which
`a14_row53_conserved` section 6 explicitly listed as **outside** its bound.
Arm `a15_nonabelian_invariant`.  Date 2026-08-30.  Modal $0.  Paid
model-provider calls $0.  No `sorry`, no proof artifact, no missing lemma.

**Read the kill and the search in this order and do not invert them.**  The
arm dies at the orbit-phase bound (section 4), which is independent of window
width, of the monoid, and of the search.

**This is NOT an absence result, and must not be written up as one.**  In the
non-group monoids the search returned **1,988 transfer invariants of Rule 30**
that survive `(*)` on three independent fresh banks and on a wide/dense/
multi-clump stress test none of the banks covered (section 7.2).  They are real.
They are also worth nothing, for two independently sufficient reasons measured
per survivor: the orbit-phase bound caps each at `<= 1.585` bits about the
entire orbit, and each is column-blind — **0 of 1,988 show any column-0
disagreement at `W >= 64`**, the maximum anywhere being `0.00995` — two rows out
of 201, at `W = 32` alone, and exactly `0` at `W = 64, 128, 256`.  That is a
couple of rows, not a measured `1/W` curve, and is not described as one.  In every *group* cell there is genuine absence, proved
by set equality with the coboundary space.

**The one thing a15 corrects in the repo:** `PATH.md` section 0.1's `O(1/W)`
single-column gate is a filter on *normalised, real-valued* functionals.  It
does not bind exact algebraic invariants — not the non-abelian ones this arm
searched, and **not a14's own abelian site sums either**, once those are read
mod `m` instead of as a density.  Section 3 measures both, side by side, on
the same diagram, with the same harness.

---

## 1. The object, defined before searching

Fix a finite monoid `M` with identity `e`, a window width `w`, and a map
`phi: {0,1}^w -> M` with `phi(0^w) = e`.  For a finite-support configuration
`s` over a quiescent background define the **ordered product**

```
Phi(s)  =  ...  phi(s[x-1 .. x+w-2]) * phi(s[x .. x+w-1]) * phi(s[x+1 .. x+w]) ...
```

multiplied left to right.  It is a finite product because all but finitely
many factors are `e`.  Equivalently: `phi` is the transition function of a
finite automaton and `Phi(s)` is the transformation that automaton performs
reading the row left to right.

`Phi` is a **transfer invariant** iff there is a function `f: M -> M` with

```
    Phi(F(s))  =  f(Phi(s))       for every finite-support s.          (*)
```

`f` is **not stipulated**.  It is reconstructed from the data as a partial
function on the observed image, and (*) fails the instant two configurations
with equal `Phi` have successors with unequal `Phi`.  This is deliberately
more permissive than a14's `Phi(F(s)) = Phi(s)`: it subsumes exact invariance
(`f = id`), invariance up to a twist (`f` an automorphism), invariance up to
conjugation (`f = x -> g x g^-1`), and even collapsing `f`.  **Absence under a
more permissive definition is a stronger absence.**  It also matters
concretely: section 6's Rule 90 excess consists entirely of collapsing `f`,
which a14's definition would not have seen at all.

**Derived lemma, verified in code, not assumed.**  If `s` and `s'` have
supports separated by more than `w` cells then `Phi(s u s') = Phi(s) Phi(s')`,
and after one step the two light cones are still separated by more than `w`,
so (*) forces `f(Phi(s)Phi(s')) = f(Phi(s)) f(Phi(s'))`.  **`f` must be a
homomorphism on the image submonoid**, and anti-homomorphisms are excluded
unless the image is commutative.  A homomorphism violation is therefore a
*proof* of non-conservation, and the search uses it as an independent filter:
disjoint-union pairs are put in the configuration bank so the constraint is
exercised, and any candidate violating it is discarded as a false survivor
(this fired: 50 of 15,270 in the rule-184 control at `T3`, `w = 3`).

**Triviality ladder, pre-registered in `search.py`'s docstring before running.**

| | test | why it is trivial |
|---|---|---|
| **T1** | `\|image\| = 1`, i.e. `Phi == e` | carries nothing.  Coboundaries `phi(v) = h(v_0..v_{w-2}) h(v_1..v_{w-1})^{-1}` telescope to `e` on finite support and land here |
| **T2** | `Phi(row_t)` eventually constant on the lone-seed orbit | no per-row information.  An absorbing zero in the image makes `Phi` the indicator "does the row contain word `v`", which is eventually constant |
| **T3** | flipping interior cells (more than `w` from both ends of the support) never moves `Phi` | an end-reader.  A rank-1 element absorbs one side; such a `Phi` is column-blind and dies at step 0 anyway |
| **T4** | the submonoid generated by the image is commutative | an abelian site sum in disguise.  **Bucketed, not discarded** — a14 covers only `Z/2` and `Z/3`, so a commutative find in `Z/4`, `Z/5`, `Z/6` or `Z/2xZ/2` would still be new territory |

---

## 2. Why this is a different object from a14, and not a wider version of it

a14 searched **abelian site-sum** aggregates `Phi(s) = sum_x phi(...)` valued
in `Z`, `Z/2`, `Z/3`, and answered them completely by linear algebra on the de
Bruijn graph.  That method does not apply here: monoid composition is not
linear, so there is no kernel to compute and no continuity equation to solve.
The two arms also differ in what they can see — a14's `f` is forced to be the
identity, this arm's is an unknown function reconstructed from data.

They are nevertheless commensurable, which is the point of section 5.2: on the
overlap (`G = Z/2`, `Z/3`) the two independent methods must agree, and they do,
to the exact count.

---

## 3. STEP 0, the mandatory gate: it SURVIVED, and the reason retires a repo assumption

`step0_gate.py`, log `step0_gate.log`.  Harness: the mandated
`experiments/rule30/p_geometric_attack/discriminator.py`, imported READ-ONLY,
using its `diagram`, `overwrite_centre` and `s0_control`.  `A` = true Rule 30
lone seed, `B` = `A` with column 0 overwritten by `0101...`, `C` = Rule 90 lone
seed.  `T = 400`; 196 of 324,409 cells change from `A` to `B` (fraction
`6.04e-4`), and the harness asserts the two fields differ on column 0 and
nowhere else.  `s0_control` reproduces a14's `absAB = 0.488778` exactly, which
is the cross-check that both arms are reading the same column of the same
diagram.

A monoid element is not a number, so the honest sensitivity metric is exact
disagreement, not a difference of reals:

```
disagree(W)  =  fraction of rows t in [T/2, T) with  Q(A_t) != Q(B_t)
```

on a width-`W` window about the centre.  The column-0 positive control in that
same metric is `Q(row) = the centre bit`.

**Pre-registered before the run** (`step0_gate.py` docstring): P1 the
non-abelian product is flat in `W`; P2 a14's abelian site sum read *exactly*
(mod 2, unnormalised) is *also* flat; P3 the same sum read as a *normalised
real density* decays like `1/W`.  Kill condition: if the monoid product decays
like `1/W` against a flat control, obstruction C retires the class and the arm
stops without searching.

### Measured

| quantity | W=32 | W=64 | W=128 | W=256 | behaviour |
|---|---|---|---|---|---|
| **COL0_control_centre_bit** (positive control) | **0.5224** | **0.5224** | **0.5224** | **0.5224** | **flat** |
| `NONAB_S3_w2_rand0` | 0.5224 | 0.5224 | 0.5224 | 0.5224 | **flat** |
| `NONAB_S3_w3_rand0` | 0.4925 | 0.4925 | 0.4925 | 0.4925 | **flat** |
| `NONAB_S3_w3_rand1` | 0.3831 | 0.3831 | 0.3831 | 0.3831 | **flat** |
| `NONAB_S3_w3_structured` | 0.4876 | 0.4876 | 0.4876 | 0.4876 | **flat** |
| `AB_Z2_block11_exact` (a14's `phi_w2_block11`, **mod 2**) | 0.2537 | 0.2537 | 0.2537 | 0.2537 | **flat** |
| `AB_Z2_monomial3_exact` (a14's `phi_w3_monomial`, **mod 2**) | 0.2338 | 0.2338 | 0.2338 | 0.2338 | **flat** |
| `AB_density_normalised` (**the same `phi`, as a real density**) `absAB` | 0.01757 | 0.008784 | 0.004392 | 0.002196 | **halves per doubling** |
| `AB_monomial3_normalised` `absAB` | 0.01364 | 0.006712 | 0.003330 | 0.001658 | **halves per doubling** |
| `s0_control` (a14's harness statistic) `absAB` | 0.488778 | 0.488778 | 0.488778 | 0.488778 | flat |

**KILL CONDITION DID NOT FIRE.**  Read the last three rows together: the same
`phi`, on the same diagram, is column-blind as a normalised density and
column-sensitive as an exact element of `Z/2`.  The `O(1/W)` in a14 section
2.2 comes from the explicit `1/W` in its definition of `Phi_W`, not from the
algebra.  In a group, `Phi_W(B) = L (g^-1 g') R`: nothing in that expression
shrinks with `W`.

**Consequences, stated so neither is over-read.**

1. `PATH.md` 0.1 / obstruction C, as operationalised, is a filter on
   *continuous, normalised* functionals.  Exact algebraic invariants — abelian
   or not — pass it.  a14's operative kill was its section 2.1 support-growth
   argument, which is a different argument; a14 section 2.2's `O(1/W)` bound is
   correct for the statistic it defines and does not generalise to the exact
   reading.  Nothing in a14's verdict changes: section 2.1 still carries it.
2. Passing step 0 is **necessary, not sufficient**.  It says the class is not
   retired in advance.  It says nothing about whether a member exists, and
   nothing about whether a member would decide P1.  Section 4 answers the
   second question and section 5 the first.
3. The sub-class with an absorbing/rank-1 element is column-blind and *does*
   die here: `NONAB_T2_*`, `NONAB_T3_*` and `NONAB_FlipFlop3_*` report
   `disagreeAB` of `0.0` or `0.005` at every `W`.  These are the end-readers of
   T3, caught by step 0 independently.  That is the trap the gate exists for,
   firing on the sub-class it applies to and not on the one it does not.
4. **The class-level pass did NOT extend to the survivors, and this is the
   single most important sentence in the document.**  The `phi` that pass step
   0 here are drawn at random from the whole class; conservation is a severe
   constraint, and the `phi` that actually satisfy `(*)` for Rule 30 turn out
   to be exactly the low-rank, forgetful ones — of which **not one** moves when
   column 0 is overwritten at `W >= 64` (section 7.2).  A class-level step-0
   pass is a licence to search, never a property of what the search returns.
   That is why the per-survivor re-run (R2) is part of the protocol and was
   written into `inspect_finds.py` before any candidate had been triaged.  The
   wide-configuration stress (R4) was NOT: it was added after the survivors
   appeared, in order to break them, and failed to.

---

## 4. THE KILL: the orbit-phase bound

`orbit_bound.py`, log `orbit_bound.log`, data `orbit_bound.json`.

**Proposition.**  Let `Phi` be any transfer invariant in the class of section 1
— any finite monoid `M`, any width `w`, any `phi`.  Write `m_0 = Phi(row_0)`
for the lone seed.  Then by (*), immediately and by induction,

```
    Phi(row_t)  =  f^t(m_0)      for every t.
```

`f^t(m_0)` is the trajectory of a map of a set of size `|M|` into itself,
hence eventually periodic with `preperiod + period <= |M|`.

**Consequences.**

* **(a)** `Phi(row_t)` is computable in `O(|M|)` work *without simulating Rule
  30*.  It is a function of `t` and the phase alone.
* **(b)** The invariant's **total** information about the entire orbit
  `row_0, row_1, row_2, ...` is at most `log2 |M|` bits: 1 bit for `|M| = 2`,
  **2.585 bits for `|M| <= 6`**, 4.755 bits for `|M| <= 27`.  Not per row —
  in total, for all time.
* **(c)** The single equation the invariant supplies at row `t` is
  `L * phi(window at column 0) * R = f^t(m_0)`, with `L` and `R` ordered
  products over the `~2t` other cells of the row.  Solving it for column 0
  requires `L` and `R`, i.e. requires the rest of the row already.

This is the exact-constraint analogue of a14 section 2.1's support-growth
asymmetry, and it is **sharper**: the total budget is named rather than bounded
asymptotically.  It is independent of `w`, so it closes every width past the
searched frontier, and independent of `M` beyond a logarithm, so it closes
every monoid including all the ones not enumerated.  **This is the verdict.**

**The seam with section 3, which must not be read as a contradiction.**  Step 0
measures a **windowed** readout `Phi_W` on a width-`W` window about the centre;
there `L` and `R` are products over unconstrained cells, so `Phi_W` moves when
column 0 moves.  The searched object is the **full-row** product, whose value
conservation pins to `f^t(m_0)`.  Both statements are true of the same `phi`:
the windowed readout is column-sensitive (so the class clears `PATH.md` 0.1),
and the full-row invariant carries `<= log2|M|` bits about the whole orbit (so
it decides nothing).

### Verification of the proposition, three parts

| check | result |
|---|---|
| **combinatorial core, exhaustive**: every map of an `n`-set to itself, every start, `n = 2..6` (`4 + 27 + 256 + 3125 + 46656 = 50,068` maps) | worst `preperiod + period` = `n` in every case, never more.  **0 violations** |
| **premise chain on a rule where invariants DO exist** (rule 184, number-conserving): find its nontrivial transfer invariants with the same pipeline, then profile long orbits | `S3 w=2`: 30 found; `S3 w=3`: 1,080 found; `Z3 w=2`: 6 found.  36 orbits x 400 steps.  **0 bound violations**; max `preperiod+period` = 1; max realised information **0.0 bits** against a 2.585-bit ceiling |
| **Rule 30's own survivors**, same measurement (`Z3 w=3`, `S3 w=3`, `Z6 w=3`) | 48 orbits x 400 steps; every profiled orbit **constant**; max realised information **0.0 bits** |

The rule-184 line is the load-bearing one: on a rule that genuinely has
non-abelian transfer invariants, the bound is not merely satisfied, it is
saturated at the trivial end.

---

## 5. The search: exhaustive ABSENCE in every group cell, and 1,988 found invariants in the non-group ones

`search.py`, log `search.log`, data `results.jsonl`; summary `verify.py`.
Pipeline order (cheapest disconfirming test first): `f` well-defined over a
364-pair configuration bank with early exit → lone-seed orbit → interior
probes → triviality ladder → homomorphism lemma → per-survivor triage
(section 7).

Bank composition, per `(rule, w)`: 260 random finite-support configurations of
width 3..16, 44 consecutive lone-seed orbit pairs, and 60 disjoint unions of
two random configs separated by `w+2` zeros (these are what exercise the
homomorphism lemma).  Plus a 60-row lone-seed orbit and 90 single-interior-cell
probe pairs.

### 5.1 THE BOUND, stated exactly

Enumerated monoids: **every group of order `<= 6` up to isomorphism**.  The
complete list is `Z/1, Z/2, Z/3, Z/4, Z/2xZ/2, Z/5, Z/6, S_3`, of which `S_3`
is the only non-abelian one; the seven nontrivial ones are searched, and `Z/1`
is omitted because its only `phi` is the constant `e`, which is T1 by
definition and carries nothing.  Plus the full transformation monoids `T_2`
(4 elements) and `T_3` (27), plus the flip-flop monoid `FlipFlop3` (3), the
canonical end-reader, included as a deliberate positive control for the T3
triviality.  `monoids.py` verifies identity, associativity and the group
axioms for all eleven.

**"All monoids of order `<= 6`" was not attempted and is not claimed.**  A
faithful Cayley representation of an arbitrary 6-element monoid needs `T_6`
(46,656 elements), and the number of 6-element semigroups up to isomorphism is
in the tens of millions; neither is enumerable this way.  What *is* covered is
stated above, and section 4 covers the rest regardless.

**Widths.**  `w = 1..6` for the eight groups and for `T2` under Rule 30;
`w = 1..4` for `T3`; `w = 1..3` for `FlipFlop3` and for `T2`/`T3`/`FlipFlop3`
under Rule 90.  The omitted non-group cells at `w >= 4` were dropped for
runtime and, per section 5.3, carry no coverage in any case: in those monoids
nearly every random `phi` survives as an end-reader, so the cell costs hours
and its result is `E[informative hits] = ` nothing.

**Totals: 15,289,954 candidates in the main search plus 253,512 in the control
battery.  Strictly-nontrivial candidates surviving the ladder: ZERO in every
group cell for both rules, over 6,706,598 candidates per rule.**  The 314
(Rule 30) and 1 (Rule 90) strict candidates all lie in the non-group monoids
`T2` and `T3`, and every one of them is triaged in section 7.2.

| rule | monoid | `\|M\|` | w | mode | candidates | survivors | T1 | predicted | matches | strict finds | E[coboundary hits] |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 30 | `Z2` | 2 | 1 | exhaustive | 2 | 1 | 1 | 1 | **yes** | 0 | exhaustive |
| 30 | `Z2` | 2 | 2 | exhaustive | 8 | 2 | 2 | 2 | **yes** | 0 | exhaustive |
| 30 | `Z2` | 2 | 3 | exhaustive | 128 | 8 | 8 | 8 | **yes** | 0 | exhaustive |
| 30 | `Z2` | 2 | 4 | exhaustive | 32,768 | 128 | 128 | 128 | **yes** | 0 | exhaustive |
| 30 | `Z2` | 2 | 5 | sampled | 300,000 | 4 | 4 | — | — | 0 | 4.58 |
| 30 | `Z2` | 2 | 6 | sampled | 300,000 | 0 | 0 | — | — | 0 | 6.98e-05 |
| 30 | `Z3` | 3 | 1 | exhaustive | 3 | 1 | 1 | 1 | **yes** | 0 | exhaustive |
| 30 | `Z3` | 3 | 2 | exhaustive | 27 | 3 | 3 | 3 | **yes** | 0 | exhaustive |
| 30 | `Z3` | 3 | 3 | exhaustive | 2,187 | 27 | 27 | 27 | **yes** | 0 | exhaustive |
| 30 | `Z3` | 3 | 4 | sampled | 300,000 | 48 | 48 | — | — | 0 | 45.7 |
| 30 | `Z3` | 3 | 5 | sampled | 300,000 | 0 | 0 | — | — | 0 | 0.00697 |
| 30 | `Z3` | 3 | 6 | sampled | 300,000 | 0 | 0 | — | — | 0 | 1.62e-10 |
| 30 | `Z4` | 4 | 1 | exhaustive | 4 | 1 | 1 | 1 | **yes** | 0 | exhaustive |
| 30 | `Z4` | 4 | 2 | exhaustive | 64 | 4 | 4 | 4 | **yes** | 0 | exhaustive |
| 30 | `Z4` | 4 | 3 | exhaustive | 16,384 | 64 | 64 | 64 | **yes** | 0 | exhaustive |
| 30 | `Z4` | 4 | 4 | sampled | 300,000 | 5 | 5 | — | — | 0 | 4.58 |
| 30 | `Z4` | 4 | 5 | sampled | 300,000 | 0 | 0 | — | — | 0 | 6.98e-05 |
| 30 | `Z4` | 4 | 6 | sampled | 300,000 | 0 | 0 | — | — | 0 | 1.63e-14 |
| 30 | `Z2xZ2` | 4 | 1 | exhaustive | 4 | 1 | 1 | 1 | **yes** | 0 | exhaustive |
| 30 | `Z2xZ2` | 4 | 2 | exhaustive | 64 | 4 | 4 | 4 | **yes** | 0 | exhaustive |
| 30 | `Z2xZ2` | 4 | 3 | exhaustive | 16,384 | 64 | 64 | 64 | **yes** | 0 | exhaustive |
| 30 | `Z2xZ2` | 4 | 4 | sampled | 300,000 | 7 | 7 | — | — | 0 | 4.58 |
| 30 | `Z2xZ2` | 4 | 5 | sampled | 300,000 | 0 | 0 | — | — | 0 | 6.98e-05 |
| 30 | `Z2xZ2` | 4 | 6 | sampled | 300,000 | 0 | 0 | — | — | 0 | 1.63e-14 |
| 30 | `Z5` | 5 | 1 | exhaustive | 5 | 1 | 1 | 1 | **yes** | 0 | exhaustive |
| 30 | `Z5` | 5 | 2 | exhaustive | 125 | 5 | 5 | 5 | **yes** | 0 | exhaustive |
| 30 | `Z5` | 5 | 3 | exhaustive | 78,125 | 125 | 125 | 125 | **yes** | 0 | exhaustive |
| 30 | `Z5` | 5 | 4 | sampled | 300,000 | 1 | 1 | — | — | 0 | 0.768 |
| 30 | `Z5` | 5 | 5 | sampled | 300,000 | 0 | 0 | — | — | 0 | 1.97e-06 |
| 30 | `Z5` | 5 | 6 | sampled | 300,000 | 0 | 0 | — | — | 0 | 1.29e-17 |
| 30 | `Z6` | 6 | 1 | exhaustive | 6 | 1 | 1 | 1 | **yes** | 0 | exhaustive |
| 30 | `Z6` | 6 | 2 | exhaustive | 216 | 6 | 6 | 6 | **yes** | 0 | exhaustive |
| 30 | `Z6` | 6 | 3 | exhaustive | 279,936 | 216 | 216 | 216 | **yes** | 0 | exhaustive |
| 30 | `Z6` | 6 | 4 | sampled | 300,000 | 0 | 0 | — | — | 0 | 0.179 |
| 30 | `Z6` | 6 | 5 | sampled | 300,000 | 0 | 0 | — | — | 0 | 1.06e-07 |
| 30 | `Z6` | 6 | 6 | sampled | 300,000 | 0 | 0 | — | — | 0 | 3.77e-20 |
| 30 | `S3` | 6 | 1 | exhaustive | 6 | 1 | 1 | 1 | **yes** | 0 | exhaustive |
| 30 | `S3` | 6 | 2 | exhaustive | 216 | 6 | 6 | 6 | **yes** | 0 | exhaustive |
| 30 | `S3` | 6 | 3 | exhaustive | 279,936 | 216 | 216 | 216 | **yes** | 0 | exhaustive |
| 30 | `S3` | 6 | 4 | sampled | 300,000 | 0 | 0 | — | — | 0 | 0.179 |
| 30 | `S3` | 6 | 5 | sampled | 300,000 | 0 | 0 | — | — | 0 | 1.06e-07 |
| 30 | `S3` | 6 | 6 | sampled | 300,000 | 0 | 0 | — | — | 0 | 3.77e-20 |
| 30 | `T2` | 4 | 1 | exhaustive | 4 | 3 | 3 | — | — | 0 | exhaustive |
| 30 | `T2` | 4 | 2 | exhaustive | 64 | 50 | 42 | — | — | 0 | exhaustive |
| 30 | `T2` | 4 | 3 | exhaustive | 16,384 | 11,784 | 9,928 | — | — | 0 | exhaustive |
| 30 | `T2` | 4 | 4 | sampled | 300,000 | 205,952 | 177,036 | — | — | 5 | no calibration |
| 30 | `T2` | 4 | 5 | sampled | 300,000 | 203,265 | 175,826 | — | — | 0 | no calibration |
| 30 | `T2` | 4 | 6 | sampled | 300,000 | 202,959 | 175,920 | — | — | 6 | no calibration |
| 30 | `T3` | 27 | 1 | exhaustive | 27 | 16 | 10 | — | — | 0 | exhaustive |
| 30 | `T3` | 27 | 2 | exhaustive | 19,683 | 8,673 | 4,965 | — | — | 72 | exhaustive |
| 30 | `T3` | 27 | 3 | sampled | 300,000 | 93,136 | 65,135 | — | — | 208 | no calibration |
| 30 | `T3` | 27 | 4 | sampled | 300,000 | 76,271 | 61,411 | — | — | 23 | no calibration |
| 30 | `FlipFlop3` | 3 | 1 | exhaustive | 3 | 3 | 3 | — | — | 0 | exhaustive |
| 30 | `FlipFlop3` | 3 | 2 | exhaustive | 27 | 27 | 23 | — | — | 0 | exhaustive |
| 30 | `FlipFlop3` | 3 | 3 | exhaustive | 2,187 | 1,989 | 1,717 | — | — | 0 | exhaustive |
| 90 | `Z2` | 2 | 1 | exhaustive | 2 | 2 | 1 | 2 | **yes** | 0 | exhaustive |
| 90 | `Z2` | 2 | 2 | exhaustive | 8 | 4 | 2 | 4 | **yes** | 0 | exhaustive |
| 90 | `Z2` | 2 | 3 | exhaustive | 128 | 16 | 8 | 16 | **yes** | 0 | exhaustive |
| 90 | `Z2` | 2 | 4 | exhaustive | 32,768 | 256 | 128 | 256 | **yes** | 0 | exhaustive |
| 90 | `Z2` | 2 | 5 | sampled | 300,000 | 10 | 4 | — | — | 0 | 9.16 |
| 90 | `Z2` | 2 | 6 | sampled | 300,000 | 0 | 0 | — | — | 0 | 0.00014 |
| 90 | `Z3` | 3 | 1 | exhaustive | 3 | 1 | 1 | 1 | **yes** | 0 | exhaustive |
| 90 | `Z3` | 3 | 2 | exhaustive | 27 | 3 | 3 | 3 | **yes** | 0 | exhaustive |
| 90 | `Z3` | 3 | 3 | exhaustive | 2,187 | 27 | 27 | 27 | **yes** | 0 | exhaustive |
| 90 | `Z3` | 3 | 4 | sampled | 300,000 | 48 | 48 | — | — | 0 | 45.7 |
| 90 | `Z3` | 3 | 5 | sampled | 300,000 | 0 | 0 | — | — | 0 | 0.00697 |
| 90 | `Z3` | 3 | 6 | sampled | 300,000 | 0 | 0 | — | — | 0 | 1.62e-10 |
| 90 | `Z4` | 4 | 1 | exhaustive | 4 | 2 | 1 | 2 | **yes** | 0 | exhaustive |
| 90 | `Z4` | 4 | 2 | exhaustive | 64 | 8 | 4 | 8 | **yes** | 0 | exhaustive |
| 90 | `Z4` | 4 | 3 | exhaustive | 16,384 | 128 | 64 | 128 | **yes** | 0 | exhaustive |
| 90 | `Z4` | 4 | 4 | sampled | 300,000 | 11 | 5 | — | — | 0 | 9.16 |
| 90 | `Z4` | 4 | 5 | sampled | 300,000 | 0 | 0 | — | — | 0 | 0.00014 |
| 90 | `Z4` | 4 | 6 | sampled | 300,000 | 0 | 0 | — | — | 0 | 3.25e-14 |
| 90 | `Z2xZ2` | 4 | 1 | exhaustive | 4 | 4 | 1 | 4 | **yes** | 0 | exhaustive |
| 90 | `Z2xZ2` | 4 | 2 | exhaustive | 64 | 16 | 4 | 16 | **yes** | 0 | exhaustive |
| 90 | `Z2xZ2` | 4 | 3 | exhaustive | 16,384 | 256 | 64 | 256 | **yes** | 0 | exhaustive |
| 90 | `Z2xZ2` | 4 | 4 | sampled | 300,000 | 22 | 7 | — | — | 0 | 18.3 |
| 90 | `Z2xZ2` | 4 | 5 | sampled | 300,000 | 0 | 0 | — | — | 0 | 0.000279 |
| 90 | `Z2xZ2` | 4 | 6 | sampled | 300,000 | 0 | 0 | — | — | 0 | 6.51e-14 |
| 90 | `Z5` | 5 | 1 | exhaustive | 5 | 1 | 1 | 1 | **yes** | 0 | exhaustive |
| 90 | `Z5` | 5 | 2 | exhaustive | 125 | 5 | 5 | 5 | **yes** | 0 | exhaustive |
| 90 | `Z5` | 5 | 3 | exhaustive | 78,125 | 125 | 125 | 125 | **yes** | 0 | exhaustive |
| 90 | `Z5` | 5 | 4 | sampled | 300,000 | 1 | 1 | — | — | 0 | 0.768 |
| 90 | `Z5` | 5 | 5 | sampled | 300,000 | 0 | 0 | — | — | 0 | 1.97e-06 |
| 90 | `Z5` | 5 | 6 | sampled | 300,000 | 0 | 0 | — | — | 0 | 1.29e-17 |
| 90 | `Z6` | 6 | 1 | exhaustive | 6 | 2 | 1 | 2 | **yes** | 0 | exhaustive |
| 90 | `Z6` | 6 | 2 | exhaustive | 216 | 12 | 6 | 12 | **yes** | 0 | exhaustive |
| 90 | `Z6` | 6 | 3 | exhaustive | 279,936 | 432 | 216 | 432 | **yes** | 0 | exhaustive |
| 90 | `Z6` | 6 | 4 | sampled | 300,000 | 0 | 0 | — | — | 0 | 0.357 |
| 90 | `Z6` | 6 | 5 | sampled | 300,000 | 0 | 0 | — | — | 0 | 2.13e-07 |
| 90 | `Z6` | 6 | 6 | sampled | 300,000 | 0 | 0 | — | — | 0 | 7.54e-20 |
| 90 | `S3` | 6 | 1 | exhaustive | 6 | 4 | 1 | 4 | **yes** | 0 | exhaustive |
| 90 | `S3` | 6 | 2 | exhaustive | 216 | 24 | 6 | 24 | **yes** | 0 | exhaustive |
| 90 | `S3` | 6 | 3 | exhaustive | 279,936 | 864 | 216 | 864 | **yes** | 0 | exhaustive |
| 90 | `S3` | 6 | 4 | sampled | 300,000 | 0 | 0 | — | — | 0 | 0.714 |
| 90 | `S3` | 6 | 5 | sampled | 300,000 | 0 | 0 | — | — | 0 | 4.25e-07 |
| 90 | `S3` | 6 | 6 | sampled | 300,000 | 0 | 0 | — | — | 0 | 1.51e-19 |
| 90 | `T2` | 4 | 1 | exhaustive | 4 | 4 | 3 | — | — | 0 | exhaustive |
| 90 | `T2` | 4 | 2 | exhaustive | 64 | 48 | 42 | — | — | 0 | exhaustive |
| 90 | `T2` | 4 | 3 | exhaustive | 16,384 | 11,472 | 9,928 | — | — | 0 | exhaustive |
| 90 | `T3` | 27 | 1 | exhaustive | 27 | 25 | 10 | — | — | 0 | exhaustive |
| 90 | `T3` | 27 | 2 | exhaustive | 19,683 | 7,719 | 4,965 | — | — | 0 | exhaustive |
| 90 | `T3` | 27 | 3 | sampled | 300,000 | 84,741 | 65,135 | — | — | 1 | no calibration |
| 90 | `FlipFlop3` | 3 | 1 | exhaustive | 3 | 3 | 3 | — | — | 0 | exhaustive |
| 90 | `FlipFlop3` | 3 | 2 | exhaustive | 27 | 25 | 23 | — | — | 0 | exhaustive |
| 90 | `FlipFlop3` | 3 | 3 | exhaustive | 2,187 | 1,945 | 1,717 | — | — | 0 | exhaustive |

### 5.2 Independent cross-validation against a14, and structural identification

The null hypothesis makes a sharp, falsifiable prediction.  For a **group**
`G` of order `g`, every `h: {0,1}^{w-1} -> G` gives a coboundary
`phi_h(v) = h(v_0..v_{w-2}) h(v_1..v_{w-1})^{-1}`.  The right factor of window
`x` and the left factor of window `x+1` are the *same word*, so the product
telescopes to `h(0^{w-1}) h(0^{w-1})^{-1} = e` on every finite-support
configuration.  The map `h -> phi_h` has kernel exactly the constants, so
there are `g^(2^(w-1) - 1)` coboundaries and all are T1.  Therefore, if
nothing else exists,

```
    survivors(Rule 30, G, w)  ==  g ** (2**(w-1) - 1),  all T1-constant.
```

`coboundary_check.py` does better than compare counts: it builds the
coboundary set explicitly, checks the telescoping claim by direct simulation
(60 coboundaries x 25 random configurations per cell), and asserts **set
equality** with the search's survivor set.

| cell | `g^(2^(w-1)-1)` | coboundaries built | telescoping failures | survivors Rule 30 | **set equal** |
|---|---|---|---|---|---|
| `Z2, w=3` | 8 | 8 | 0 | 8 | **yes** |
| `Z2, w=4` | 128 | 128 | 0 | 128 | **yes** |
| `Z3, w=3` | 27 | 27 | 0 | 27 | **yes** |
| `Z4, w=3` | 64 | 64 | 0 | 64 | **yes** |
| `Z2xZ2, w=3` | 64 | 64 | 0 | 64 | **yes** |
| `Z5, w=3` | 125 | 125 | 0 | 125 | **yes** |
| `Z6, w=3` | 216 | 216 | 0 | 216 | **yes** |
| `S3, w=2` | 6 | 6 | 0 | 6 | **yes** |
| `S3, w=3` | 216 | 216 | 0 | 216 | **yes** |

So in the group cells the search's zero is not "nothing turned up".  It is
**"exactly the rule-independent trivial space turned up, and nothing else"** — the same shape
of statement a14 reached for its own class, reached here by a completely
different route (ordered products and direct simulation; no linear algebra, no
de Bruijn graph, no continuity equation).

On the overlap the two arms agree numerically: a14's finite-support dimension
is `2^(w-1) - 1` over `Z/2` and `Z/3`, i.e. `2^3 = 8` and `3^3 = 27` maps at
`w = 3`, which is what the table shows.  **`Z/4`, `Z/5`, `Z/6`, `Z/2xZ/2` and
`S_3` are new**: a14 section 6 lists composite `Z/m` and primes past 3 as
outside its bound.

### 5.3 Where the sampled cells have no power, said plainly

The candidate space has size `|M|^(2^w - 1)`.  At `w >= 4` for `|M| >= 4` a
300,000-candidate uniform sample covers a vanishing fraction, and `verify.py`
reports the calibration `E[coboundary hits] = budget * g^(2^(w-1)-1) /
g^(2^w-1)` for every sampled **group** cell.  Where that is well below 1 the
cell cannot detect even the trivial space that is known to be there, so its
zero carries no information and **is not claimed as coverage**.  Example:
`Z6, w=4` returned 0 survivors from 300,000 samples with
`E[coboundary hits] = 0.18` — consistent with zero and uninformative.  For the
sampled **non-group** cells (`T2`, `T3`, `FlipFlop3`) there is no coboundary
formula, hence no calibration at all; their zeros are likewise uninformative.

No sampling budget fixes this: the space grows as `|M|^(2^w-1)`.  **The
exhaustive frontier is the entire empirical bound.**  Section 4 is what closes
everything past it.

Note this cuts only one way.  A sampled cell's *zero* is uninformative, but a
sampled cell's *find* is a find: the 206 verified `T3, w=3` invariants of
section 7.2 came out of a sampled cell and are none the worse for it.  Sampling
under-counts; it does not manufacture.

---

## 6. The Rule 90 filter: NON-SEPARATING, the formal difference confined to the degenerate part

`rule90_extras.py`, log `rule90_extras.log`, data `rule90_extras.json`.

**The verdict first, so the table cannot be misread.  Both rules have ZERO
nontrivial transfer invariants.  The class is NON-SEPARATING and the `PATH.md`
section 0 filter closes it, exactly as it closed a14's class.**

The two rules do differ *formally*, which a14's class did not: Rule 90 has
strictly more survivors, and precisely when `G` has an element of order 2.
But the entire excess consists of invariants whose `f` is the constant map, so
it lies wholly inside the degenerate part and none of it is nontrivial.
Presenting that difference as a separation would be the exact trap `PATH.md`
7.3 C records against rows 57-59: **rule-sensitivity is not evidence of
P1-relevance.**  It is reported because the structure is clean and exact, not
because it is a route.

| cell | `\|G[2]\|` | coboundaries | survivors Rule 90 | ratio | `\|surv_90\| = \|cb\| * \|G[2]\|` | every extra has constant `f` |
|---|---|---|---|---|---|---|
| `Z2, w=3` | 2 | 8 | 16 | 2 | yes | 8/8 |
| `Z3, w=3` | 1 | 27 | 27 | 1 | yes | — (none) |
| `Z4, w=3` | 2 | 64 | 128 | 2 | yes | 64/64 |
| `Z2xZ2, w=3` | 4 | 64 | 256 | 4 | yes | 192/192 |
| `Z5, w=3` | 1 | 125 | 125 | 1 | yes | — (none) |
| `Z6, w=3` | 2 | 216 | 432 | 2 | yes | 216/216 |
| `S3, w=2` | 4 | 6 | 24 | 4 | yes | 18/18 |
| `S3, w=3` | 4 | 216 | 864 | 4 | yes | 648/648 |

Mechanism: Rule 90 is `s(t+1,x) = s(t,x-1) XOR s(t,x+1)`, so every cell of a
row contributes to exactly **two** cells of the successor.  A `phi` whose
values all square to `e` has its contributions cancel in pairs, giving
`Phi(F(s)) = e` for every `s` — a valid transfer invariant with `f` the
constant map.  **All 1,146 extras across the eight cells have a constant `f`**,
so they collapse the monoid to a point in one step, carry 0 bits, and exist
purely because Rule 90 is `GF(2)`-linear.

Reading for `PATH.md` section 0.  Rule 30's set is exactly the
rule-independent trivial core.  Rule 90's excess is an artefact of a
`GF(2)`-linearity Rule 30 does not have, and it is entirely collapsing, so
nothing in it is a Rule 30 route and nothing in it makes the class separating.
The count-level difference from a14 (which found the two rules identical) is
purely a definitional one: a14's `f = id` cannot see collapsing invariants and
this arm's reconstructed `f` can.  On the quantity that matters — nontrivial
invariants — both arms report the same thing for both rules: zero.

---

## 7. Controls, and the per-survivor triage

### 7.1 Control battery (`control_battery.jsonl`, `control_battery.log`)

45 records, 5 monoids x 3 widths x 3 rules.

| rule | why it is here | result |
|---|---|---|
| **204** (identity) | saturation: `F = id`, so *every* candidate must survive | survivors = candidates in **all 15 cells** |
| **170** (shift) | saturation: `Phi` is shift-invariant by construction | survivors = candidates in **all 15 cells** |
| **184** | proved number-conserving; genuine invariants must be found | a **proper subset** survives (e.g. `Z2 w=3`: 16 of 128; `S3 w=3`: 115 of 30,000), and nontrivial invariants are found at every monoid, **including ones with a non-commutative image** (`S3 w=3`: 99 nontrivial, only 13 with commutative image) |

The 184 line is what gives the arm's zero its meaning: **the pipeline finds
non-abelian transfer invariants when they exist.**  a14's analogous control
(`bruteforce_verified`) had near-zero power on Rule 30 and was reported as
such; this one has real power and is exercised in the same class the arm
searches.

The saturation controls cannot exercise `nontrivial_strict`, because rules 204
and 170 have a frozen or merely translating lone-seed orbit, so `T2` fires on
every one of their survivors by construction.  That is a property of the
control rules, not of the ladder, and it is why both `nontrivial` and
`nontrivial_strict` are reported separately throughout.

### 7.2 Per-survivor triage (`inspect_finds.py`, `finds_triage.json`)

`inspect_finds.py` (logs `inspect_finds.log`, `inspect_finds_strict.log`;
data `finds_triage.json`, `finds_triage_strict.json`) then `stress_wide.py`
(log `stress_wide.log`, data `stress_wide_all.json`).  Every candidate that
cleared the section-1 ladder in any cell is triaged individually — 2,555 of
them, after deduplication (`results.jsonl` and `results_strict.jsonl` re-run
the same sampled cells with the same seed and budget, so the first file's 40
stored finds per cell are literally the first 40 of the second file's full
list; `stress_wide.py` drops the 49 duplicates on
`(rule, monoid, w, phi)`).  Four filters, each able to kill on its own:

**Provenance, stated exactly.**  R0-R3 live in `inspect_finds.py` and were
written BEFORE any candidate had been triaged.  **R4 is post-hoc**: it was
written after the 72 column-sensitive-looking candidates appeared at `T3,
w = 2`, specifically to try to break them, and it killed 0 of 2,555.  A
post-hoc filter that fails to kill is stronger evidence for the survivors than
a planned one would be; calling it pre-registered would be false and would also
weaken it.

| | filter | what it tests | killed |
|---|---|---|---|
| **R0** | orbit-phase falsifier | section 4's proposition forces `preperiod + period <= \|M\|` for `Phi(row_t)`; checked on the lone seed and three random seeds over 400 steps.  A violation is a *proof* of non-conservation, sharper than counting distinct values | **0** |
| **R1** | three independent fresh banks | 1,400 random configs + 90 orbit rows + 300 disjoint unions each, ten times the search bank | **26** — 13 broke `(*)` outright (false survivors), 13 became trivial under the wider probes |
| **R4** (post-hoc) | wide/dense/multi-clump stress | the regime NO bank covered: 50 uniform configs at each of widths 200, 800, 2000, plus 50 configs of 4-6 clumps (which exercises the homomorphism lemma at arity 4-6, not 2) | **0** of 2,555 |
| **R2** | step 0, per survivor | the mandated `discriminator.py` fields A/B, `disagreeAB` at `W = 32..256` | see below — this is what kills every Rule 30 survivor |

R1 is the only filter that killed anything, and the post-hoc R4 killed
nothing, which says the search bank was already adequate: the survivors are
real.

### The 1,988 Rule 30 invariants, and why they are worth nothing

| rule | monoid | w | verified | max `disagreeAB` over all `W` | `disagreeAB` at `W=256` | how many nonzero at `W >= 64` | `f != id` | max orbit information |
|---|---|---|---|---|---|---|---|---|
| 30 | `FlipFlop3` | 2 | 2 | 0.000000 | 0.000000 | 0 | 0 | 1.000 bits |
| 30 | `FlipFlop3` | 3 | 22 | 0.000000 | 0.000000 | 0 | 0 | 1.000 |
| 30 | `T2` | 2 | 4 | 0.000000 | 0.000000 | 0 | 0 | 1.000 |
| 30 | `T2` | 3 | 160 | 0.000000 | 0.000000 | 0 | 0 | 1.000 |
| 30 | `T2` | 4 | 4 | 0.000000 | 0.000000 | 0 | 4 | 1.000 |
| 30 | `T3` | 2 | 1,584 | 0.004975 | 0.000000 | 0 | 72 | 1.585 |
| 30 | `T3` | 3 | 206 | 0.009950 | 0.000000 | 0 | 206 | 1.585 |
| 30 | `T3` | 4 | 6 | 0.000000 | 0.000000 | 0 | 6 | 1.585 |
| **90** | `T2` | 3 | 8 | **0.522388** | **0.522388** | **8** | 8 | 1.000 |
| **90** | `T3` | 2 | 558 | **0.522388** | **0.522388** | **558** | 558 | 1.000 |
| **90** | `T3` | 3 | 1 | **0.522388** | **0.522388** | **1** | 1 | 1.585 |

**Rule 30: 1,988 verified transfer invariants, ZERO of which disagree on
column 0 at any `W >= 64`.**  The largest disagreement anywhere in the family
is `0.00995` — two rows out of 201, at `W = 32` only, vanishing at every larger
window.  Compare the positive control, `0.5224`, flat in `W`.  Each also
carries at most `1.585` bits about the entire orbit.  So both kills apply to
every survivor individually, not merely to the class.

**Rule 90: 567 verified transfer invariants, ALL 567 column-sensitive at
`0.522388` — the positive-control value exactly, flat in `W`.**  The one rule
in the pair whose invariants can see column 0 is the rule whose centre column
is trivially eventually periodic, and even there they carry `<= 1.585` bits
and are eventually constant along the orbit.  That is the `PATH.md` section 0
filter firing as hard as it is able to.

### What the surviving objects actually are

`f != id` in 288 of the Rule 30 cases: these satisfy
`Phi(row_{t+1}) = f(Phi(row_t))` with `f` a nontrivial map, i.e. **conservation
up to a fixed drift**, which a14's `f = id` definition structurally could not
see.  That is a real class extension and it is this arm's positive
contribution.  Inspecting them (`stress_wide_all.json`), their images consist
of low-rank transformations of the 3-point set — e.g. `phi` sending the four
width-2 windows `00,01,10,11` to `(0,1,2), (0,0,1), (0,2,1), (0,2,0)` in `T3`,
whose image `{(0,0,0), (0,0,1), (0,0,2)}` is a set of rank-`<= 2` maps.  Such a
`Phi` reads the row through a bounded-memory automaton that forgets almost
everything, which is exactly why `disagreeAB` collapses to zero: the
information column 0 contributes is destroyed by the low-rank composition
before the product ends.  This is the same structural fact the orbit-phase
bound expresses from the other side.

---

## 8. Files, reproduction, fence

```
monoids.py            monoid constructions + axiom self-test (uv run python monoids.py)
substrate.py          bit-list ECA stepper, validated against common/rule30.py
step0_gate.py         the mandatory gate; imports discriminator.py READ-ONLY
step0_gate.log        its output (the section 3 table)
search.py             the bounded search; the object and ladder are in its docstring
results.jsonl         rules 30 and 90 x 10 monoids x w = 1..6
search.log            stdout of the above
control_battery.jsonl rules 204, 170, 184 x 5 monoids x w = 1..3
orbit_bound.py        the section-4 kill and its three verifications
orbit_bound.log/.json
coboundary_check.py   structural identification of the survivor set
coboundary_check.log/.json
rule90_extras.py      characterisation of Rule 90's excess
rule90_extras.log/.json
results_strict.jsonl  the same sampled cells re-run with --finds-cap 20000 so
                      every strictly-nontrivial candidate is stored, not 40
inspect_finds.py      per-survivor R0 orbit-phase falsifier, R1 fresh-bank
                      retest, R2 individual step 0, R3 orbit information
finds_triage.json, finds_triage_strict.json
inspect_finds.log, inspect_finds_strict.log
stress_wide.py        R4: wide/dense/multi-clump regime no bank covered
stress_wide.log, stress_wide_all.json, triage_summary.txt
verify.py             the summary table, with the sampling-power calibration
verify.log
table.md              the section-5.1 table, generated from results.jsonl
search_part1.log      stdout of the first (interrupted) main-search chain;
                      results.jsonl is append-only across the chain restarts
stress_wide.json      the R4 run over finds_triage.json alone; superseded by
                      stress_wide_all.json, which adds finds_triage_strict.json
                      and deduplicates
```

```
cd experiments/overnight-arms/frontier_attack/a15_nonabelian_invariant
PYTHONDONTWRITEBYTECODE=1 uv run python monoids.py
PYTHONDONTWRITEBYTECODE=1 uv run python substrate.py
PYTHONDONTWRITEBYTECODE=1 uv run python step0_gate.py 400
PYTHONDONTWRITEBYTECODE=1 uv run python search.py --rules 204,170,184 \
    --monoids Z2,Z3,S3,T3,FlipFlop3 --widths 1,2,3 --budget 30000 \
    --out control_battery.jsonl
PYTHONDONTWRITEBYTECODE=1 uv run python search.py --rules 30,90 --budget 300000 \
    --out results.jsonl
PYTHONDONTWRITEBYTECODE=1 uv run python orbit_bound.py
PYTHONDONTWRITEBYTECODE=1 uv run python coboundary_check.py
PYTHONDONTWRITEBYTECODE=1 uv run python rule90_extras.py
PYTHONDONTWRITEBYTECODE=1 uv run python search.py --rules 30 --monoids T2 \
    --widths 4,6 --budget 300000 --finds-cap 20000 --out results_strict.jsonl
PYTHONDONTWRITEBYTECODE=1 uv run python search.py --rules 30 --monoids T3 \
    --widths 3,4 --budget 300000 --finds-cap 20000 --append \
    --out results_strict.jsonl
PYTHONDONTWRITEBYTECODE=1 uv run python search.py --rules 90 --monoids T3 \
    --widths 3 --budget 300000 --finds-cap 20000 --append \
    --out results_strict.jsonl
PYTHONDONTWRITEBYTECODE=1 uv run python inspect_finds.py
PYTHONDONTWRITEBYTECODE=1 uv run python inspect_finds.py --sampled-only \
    --results results_strict.jsonl --out finds_triage_strict.json
PYTHONDONTWRITEBYTECODE=1 uv run python stress_wide.py \
    --triage finds_triage.json finds_triage_strict.json --out stress_wide_all.json
PYTHONDONTWRITEBYTECODE=1 uv run python verify.py
```

**Fence.**  Every write is inside
`experiments/overnight-arms/frontier_attack/a15_nonabelian_invariant/`.  No
existing file was modified; `experiments/rule30/` and `docs/` were read only.
No git commits.  Unlike a14, the mandated `exec_module` import of
`discriminator.py` wrote **no** `.pyc` under `experiments/rule30/`, because
every command is run with `PYTHONDONTWRITEBYTECODE=1`.

---

## 9. What a reader must not over-read

1. **The search did NOT come up empty, and the arm did not die because it
   did.**  It returned 1,988 verified Rule 30 transfer invariants.  The arm
   died at the orbit-phase bound of section 4 — independent of width and of
   the monoid — and, separately and per survivor, at step 0.  Reading it as an
   absence result leaves "maybe width 5" and "maybe a 7-element monoid" open;
   neither is open, because both kills apply to any invariant whatsoever.
2. **"Step 0 survived" is not "the class is alive."**  Step 0 is a necessary
   condition and the class meets it.  Section 4 is the sufficient reason it
   still decides nothing.  Passing a filter that retires families in advance
   only means the arm had to be evaluated on its merits, which it then was.
3. **The section-3 correction does not overturn a14.**  a14's `O(1/W)` bound
   is correct for the normalised statistic a14 defines.  What section 3 shows
   is that the bound does not extend to the exact reading of the same `phi`,
   so `PATH.md` 0.1 should be understood as scoped to normalised functionals.
   a14's verdict rests on its section 2.1, which is untouched.
4. **The Rule 90 excess in section 6 is not a Rule 30 route.**  It is the
   `GF(2)`-linearity of Rule 90 showing up as collapsing invariants.  It is
   reported because a control that fires is worth more than one that cannot.
5. **The `w >= 4` and non-group sampled cells are not coverage.**  Section 5.3
   gives the calibration; 32 of those zeros are literally uninformative.  The
   empirical *absence* bound is the exhaustive frontier only.  The *finds* from
   sampled cells are unaffected: sampling under-counts, it does not invent.
6. **"All monoids of order <= 6" was not searched** and is not claimed; see
   section 5.1 for what was.
7. **`f != id` is a real class extension, and it is still worth nothing.**  The
   288 drift invariants are objects a14's definition could not represent, and
   reporting them is the arm's positive contribution.  They are not a route:
   each carries `<= 1.585` bits about the whole orbit and none of them moves
   when column 0 is overwritten.
8. **The R1/R4 kill counts are small on purpose and are not a sign of a weak
   filter.**  R1 killed 26 and R4 killed 0 because the survivors are genuine;
   the filter with teeth here is R2, per-survivor step 0, and it is decisive.
9. **Nothing here bounds the density of ones in the centre column, and nothing
   here is a step toward P1, P2 or P3.**
