# Arm 4 iteration 2: AIR / frequency-domain search architecture

Design only. Nothing here is built. Supersedes the four-bullet sketch in
`ARM4-frequency-domain.md` §5, which is the phase-0 probe report and stays the
authority on what was measured. Companion to `SEARCH-ARCH.md` (the GF(2) seed
grammar this proposal replaces), `PREREGISTRATION.md` (the target) and
`RESULTS-arm3-run1.md` (the measured baseline).

The brief accepts the fitness corrections and pivots the grammar. The fitness
corrections carry over unchanged (§4). The grammar pivot needs four corrections
of its own before a line of it is written, and three of them are measured rather
than argued. §0 states them. §1 through §3 then write the grammar and the Z3
hook for real, as the architecture that would be built if the gate in §6 opens.

**Read §0.4 first if you read nothing else.** The transform the proposal names
does not exist in the field the proposal names.

---

## 0. Four corrections, with the evidence

### 0.1 The ordered boundary is the left one. This was measured.

The brief asks for an operator projecting "the highly-ordered right-hand
boundary" to the center column. Under the convention in `center_column.py`
(`new = (row<<1) ^ (row | (row>>1))`, position increasing rightward) the
striping is on the left and the chaos is on the right. `ARM4` §1 has the row
picture and the numbers: GF(2) linear complexity of the diagonal at depth `d` in
from each edge, over 4096 rows. Left stays at `L ~ d` out to depth 31. Right
saturates to the maximal-complexity ceiling by depth 29.

Rule 30 is left-permutive, so information propagates rightward. The ordered side
is the side information leaves, not the side it arrives at.

Swapping "right" for "left" in the brief does not rescue it, because the
objection that kills it is orientation-independent: the ordered diagonal at
depth `d` carries about `d` bits of state, and the center bit at step `n` sits at
depth `d = n`. A boundary region whose information content grows as `d` cannot
constrain a target at depth `n` any more cheaply than reading `n` bits. The
proposal reads low entropy on the ordered side as evidence that it determines the
center cheaply. It is evidence of decoupling, which is the opposite.

### 0.2 A transform changes the basis. It does not change the degree.

Algebraic degree is an invariant of the boolean function, not of the
representation chosen for it. `ARM4` §3 measured the center bit at step `t` as a
function of its `2t+1` row-0 light-cone cells: ANF degree exactly `2t-1`, two
below the ceiling, at every `t` through 10, with density plateauing near 0.15
rather than decaying. No choice of evaluation domain, basis, or field extension
moves that number.

"Closed-form frequency-domain operator `G`" is therefore not an open question in
the low-degree form the brief states it. It is measured false. The `o(n)`
prize is not measured false; the specific route is.

### 0.3 Composition squares the degree

So "no intermediate rows" and "low constraint degree" are the two ends of one
lever.

`ARM4` §0(b), restated because it is the reason the grammar in §1 cannot be
built the way the brief describes. The local rule `f(L,C,R) = L + C + R + C*R`
has degree 2. An AIR keeps it at degree 2 *by* carrying one trace row per time
step, since the transition constraint only ever relates row `t` to row `t+1`.
Eliminating intermediate rows means composing transitions, and composition
squares degree. Either degree 2 with `n` rows, or one row with degree `2^n`.
Nothing in between, and the low-degree machinery is defined on the first.

### 0.4 There are no `2^m`-th roots of unity in a binary field.

The brief asks for "evaluation over primitive roots of unity" in a binary
extension field. The multiplicative group of `GF(2^k)` is cyclic of order
`2^k - 1`, which is odd. A primitive `N`-th root of unity exists only when
`N | 2^k - 1`, so `N` must be odd. There is no primitive square root of unity,
no primitive `2^m`-th root for any `m >= 1`, and therefore no radix-2
multiplicative FFT over `GF(2^k)` at all.

This is not a performance caveat. The named primitive does not exist in the
named field, and the two halves of the brief's grammar pivot are mutually
exclusive as stated.

The replacement is real machinery and it is what §1 uses: the **additive FFT**
(Gao-Mateer, and the Lin-Chung-Han basis used by binius), which evaluates over
cosets of `F2`-linear subspaces of `GF(2^k)` instead of over a multiplicative
subgroup. Two properties matter downstream:

- It is multipoint evaluation and interpolation in `O(N log N)` field
  operations, so evaluate-multiply-interpolate polynomial multiplication works
  normally, since evaluation is a ring homomorphism and the degree bound is
  respected by construction.
- It has **no cyclic convolution theorem.** There is no wraparound structure to
  exploit, because there is no multiplicative subgroup being used. Any grammar
  primitive whose justification is "convolution becomes pointwise product in the
  transform domain" has to be restated as multipoint evaluation, and the
  restatement costs the interpolation step back.

Combined with 0.2: the transform is `F2`-linear. The `L + C + R` part passes
through it cleanly. The `C*R` term is where every difficulty lives, and a linear
change of basis does not diagonalize a nonlinear map. It spreads support rather
than sparsifying it.

---

## 1. The frequency-domain seed grammar

Three sorts. `Poly` is a univariate polynomial over `F = GF(2^k)` in coefficient
basis. `Spec` is the same object in evaluation basis over a fixed `F2`-linear
subspace `V_m <= F` of dimension `m`, so `|V_m| = 2^m` points. `Idx` is a
machine integer. The two `Poly`/`Spec` sorts are deliberately distinct so that a
derivation cannot silently treat coefficients as evaluations, which is the exact
confusion §0.4 is about.

There is still no sort for a row, a generation, or a mutable buffer, so the
exclusion that kills forward simulation (`SEARCH-ARCH.md` §1.2) survives the
pivot unchanged.

### 1.1 Primitives

```
Idx   ::= n | Lit(k) | Add(Idx,Idx) | Sub(Idx,Idx) | Half(Idx) | Log2(Idx)

Basis ::= Space(m)                      -- the F2-linear subspace V_m, dim m
        | Coset(Basis, F)               -- V_m + shift, the additive-FFT domain

Poly  ::= XCoeff(Idx)                   -- the monomial x^i
        | ConstF(F)                     -- a field constant, k <= 128 bits
        | PAdd(Poly,Poly)               -- + in F[x], characteristic 2
        | PMul(Poly,Poly)               -- * in F[x]
        | PCompose(Poly,Poly)           -- p(q(x))
        | Frob(Poly, Idx)               -- x -> x^(2^j), the Frobenius power
        | Interp(Spec, Basis)           -- additive iFFT, evaluations -> coeffs
        | Lift(Row, Basis)              -- row 0 cells -> the interpolant

Spec  ::= Eval(Poly, Basis)             -- additive FFT, coeffs -> evaluations
        | SAdd(Spec,Spec)               -- pointwise +
        | SHad(Spec,Spec)               -- pointwise * (Hadamard)
        | SShift(Spec, Idx)             -- permute the evaluation domain
        | SRule30(Spec,Spec,Spec)       -- p + q + r + q*r, pointwise
        | SSelect(Spec, Idx)            -- read one evaluation point

Row   ::= Delta                         -- the lone-1 initial configuration
```

`F` literals are capped at 128 bits, matching the `max_candidate_bytes = 64 KiB`
challenge-file cap from 61f0deb. Without both caps a candidate wins by
transcribing published center-column bits into a constant.

`Frob` is in the grammar because it is the one primitive in characteristic 2
that is genuinely free and genuinely nonlinear-looking: `x -> x^2` is
`F2`-linear on `GF(2^k)`, so squaring a polynomial is a coefficient permutation
with zero multiplications. Any real structural win in a binary field routes
through the Frobenius, so it gets a first-class primitive rather than being
reachable only as `PMul(p,p)`.

### 1.2 What the grammar has to be able to say, and the cost of saying it

Booleanity is not free here. `SEARCH-ARCH.md` worked over GF(2), where every
value is a bit by construction. Over `GF(2^k)` with `k > 1`, a trace cell must
be pinned to `{0,1}` by an explicit constraint `x^2 + x = 0`, which in
characteristic 2 is `x*(x+1) = 0`. Every cell carries one, so the arithmetization
grows a `2n+1`-wide constraint family per row that the GF(2) formulation did not
need. This is the first place the pivot costs something and it is unavoidable:
`GF(2^k)` is chosen precisely so that a polynomial can carry many cells, and the
price of a wider alphabet is having to say the alphabet is not being used.

Over a prime field the price is higher still. `ARM4` §4 records the specific
error in the earlier draft: `winter_math::fields::f64::BaseElement` is the
Goldilocks prime field, where XOR is `a + b - 2ab` and `L + C + R + C*R` is not
rule 30 at all. Characteristic 2 is not a preference here, it is a correctness
requirement, and it is why no Winterfell-backed route is available.

### 1.3 Non-vacuity, which is the acceptance test for this grammar too

`SEARCH-ARCH.md` §1.4 earned its gate by exhibiting
`Eval(Iterate(Rule30-as-map, n), Delta)`, a hand-writable term provably equal to
`a(n)`. Replacing the grammar discards that guarantee, and it has to be earned
again from scratch. A grammar that cannot express one correct program yields a
search where every candidate fails the accuracy gate forever, with no gradient,
and that failure is indistinguishable from "no shortcut exists". It is the worst
available outcome and it is the cheapest one to rule out.

The witness in this grammar is the direct arithmetization: `Lift(Delta, Space(m))`
into a `Spec` over a domain wide enough for the light cone, `SRule30` applied
`n` times pointwise, `SSelect` at the center index. It is correct, it is
`Theta(n^2)` field operations, and it is a correctness witness rather than a
competitor.

Note what writing it forces into the open. `SRule30` is pointwise, so the
witness never leaves evaluation basis and never uses `Eval`, `Interp`, or a
single FFT. **The transform is not on the path from the initial row to the
answer.** For an FFT to earn its place, a candidate has to interpolate, do
something in coefficient basis that is cheaper than `n` pointwise rounds, and
interpolate back. §0.2 and §0.3 say what that something would have to defeat.

**Gate before any search runs:** hand-write the witness above and at least one
program that actually uses `Eval`/`Interp` non-trivially and is still correct at
`n = 16`. Kill condition: no FFT-bearing correct program can be hand-written, in
which case the transform primitives are decoration and the grammar is the GF(2)
one from `SEARCH-ARCH.md` wearing a costume.

---

## 2. What Z3 can and cannot do in this field. Measured, not recalled.

The brief asks the SMT hook to "verify in the new field" instead of unrolling
boolean gates, on the stated expectation that this is cheaper. It is not, and
the direction of the error is large.

### 2.1 There is no finite-field sort in the installed solver

Measured on this machine, 2026-08-27, against `/opt/homebrew/bin/z3`, the same
binary `SEARCH-ARCH.md` §3.2 shells out to:

```
$ z3 --version
Z3 version 4.16.0 - 64 bit

$ echo '(declare-const a (_ FiniteField 7)) (check-sat)' | z3 -in
(error "line 1 column 33: unknown sort 'FiniteField'")

$ strings -a /opt/homebrew/Cellar/z3/4.16.0/bin/z3 | grep -ci finitefield
0
```

Zero matching symbols in the binary. What was measured is exactly that: no
finite-field sort of any order is reachable in the build this lab shells out to,
so no `GF(2^k)` sort is available here. Whether some other build exposes one was
not checked and does not need to be, because §2.3's conclusion follows from the
cost table in §2.2 alone. Anyone reopening this should check it rather than
inherit the assumption.

So binary-extension arithmetic reaches the solver exactly one way: bitvectors,
with carry-less multiply and explicit reduction by the field polynomial, blasted
to SAT. Every `GF(2^128)` multiply becomes a `128 x 128` AND-array plus a
127-step reduction chain, on the order of `10^4` gates, where the GF(2)
formulation used one AND.

### 2.2 The cost, measured

Same disequality shape both sides (`center bit at step n = 1`, satisfiable, so
the solver actually searches rather than closing on syntax), same generator,
`define-fun` sharing throughout so neither encoding is inflated by term
duplication. Solver cap `-T:120`, raised to `-T:300` for the last field rung.

| encoding | n | result | z3 time | SMT-LIB2 size |
|---|---|---|---|---|
| boolean, QF_UF | 8 | sat | 0.02 s | 9 KiB |
| boolean, QF_UF | 16 | sat | 0.01 s | 37 KiB |
| boolean, QF_UF | 32 | sat | 0.07 s | 149 KiB |
| boolean, QF_UF | 64 | sat | 0.62 s | 609 KiB |
| boolean, QF_UF | 128 | sat | 16.54 s | 2.5 MiB |
| `GF(2^8)` bitvector, QF_BV | 8 | sat | 1.99 s | 341 KiB |
| `GF(2^8)` bitvector, QF_BV | 16 | sat | 65.78 s | 1.3 MiB |
| `GF(2^8)` bitvector, QF_BV | 32 | timeout | > 300 s | 5.3 MiB |

The field-lifted encoding hits its wall between 16 and 32. At `n = 16` it
already costs four times what the boolean encoding costs at `n = 128`, three
doublings further up, and at `n = 32` it does not close inside 300 s. This is
at `k = 8`; the brief's field is `GF(2^128)`, where the multiply is 256 times
the AND-gate count.

`SEARCH-ARCH.md` §3.3 already noted that bounded equivalence is a small-`n`
instrument and expected `n_max` in the hundreds. The pivot moves that ceiling
from the hundreds to the low tens. Condition 1 of the claim gate asks for
`n_max >= 1024`, so the field pivot does not weaken that condition, it removes
any prospect of meeting it.

### 2.3 The correct conclusion, which is not "use a better solver"

Verification stays in GF(2) regardless of what field the candidate is written
in. This is not a compromise, it is the only coherent design: the property being
checked is a statement about bits, `GF(2^k)` cells are constrained to `{0,1}`
anyway by §1.2, and a `GF(2^k)` term whose cells are all booleanity-constrained
is semantically a boolean circuit with `k-1` wasted bits per cell. The
arithmetization is for the AIR, not for the solver.

Concretely: the term encoder emits a **projection** to GF(2) before the query.
`SHad` on booleanity-constrained operands lowers to `and`, `SAdd` to `xor`,
`SRule30` to the boolean local map, `ConstF` to its low bit if it is
`{0,1}`-valued and to a rejection otherwise. A candidate whose derivation
genuinely needs a non-`{0,1}` field element cannot be projected and is rejected
by the encoder, fail-closed, same discipline as `src/engines/formal_verification.rs`.

That rejection rule is load-bearing and worth stating as a prediction: if the
FFT primitives are doing anything, they produce non-`{0,1}` intermediates, and
the projection fails. **If in practice no candidate is ever rejected for a
non-boolean intermediate, the transform primitives are unused and §1.3's kill
condition has fired late.** Instrument the rejection counter and report it.

---

## 3. The transition constraint, stated correctly

What the brief writes as

```
x_i^(t+1) - (x_{i-1}^(t) + x_i^(t) + x_{i+1}^(t) + x_i^(t) * x_{i+1}^(t)) = 0
```

is right as algebra in characteristic 2, where `-` and `+` coincide, and it is
the constraint the AIR asserts. Three things the statement leaves out, each of
which was a concrete error in an earlier draft (`ARM4` §4) and none of which is
cosmetic.

**Trace width is `2n+1`, not a sliding window.** Each cell's successor needs its
own neighbours, so the trace has one column per light-cone position and one row
per step. The earlier 3-column draft left columns 0 and 2 unconstrained, so
every trace satisfied the AIR vacuously. The constraint above is asserted once
per interior column `i` in `1..2n-1`, per row.

**Booleanity per cell.** `x_i^(t) * (x_i^(t) + 1) = 0`, one per cell, per §1.2.
Without it the AIR admits traces over the whole field that satisfy the
transition and mean nothing.

**Boundary assertions.** Row 0 pinned to `Delta`, and the two outermost columns
pinned to 0 at every row so the light cone does not wrap.

The full AIR is then: width `2n+1`, one degree-2 transition constraint per
interior column, one degree-2 booleanity constraint per cell, boundary
assertions on row 0 and both edges. It is a correct arithmetization. It is
`Theta(n^2)` cells. It buys a proof object, not a shortcut, for the reason in
§0.3 and the reason in `ARM4` §0(a): STARK sublinearity is a **verifier**
property. The prover computes the whole trace. This lab is the party that wants
the bit, with no untrusted prover to check and no verifier to be. Asking the
prover side to inherit the verifier's cost bound is a category error rather than
an open question.

For the SMT hook, the transition constraint reaches Z3 through §2.3's
projection, at which point it is `(xor p q r (and q r))` and is exactly the
boolean unrolling from `SEARCH-ARCH.md` §3.3. Everything in §3.2 there survives
the pivot untouched: local rewrite validation, `unsat` or reject, fail-closed on
timeout or missing binary.

---

## 4. Fitness, unchanged

`SEARCH-ARCH.md` §2 carries over verbatim and is not reopened by the grammar
pivot. Restated only as a checklist so this document is self-contained on the
gate: correctness graded as `log2(n_max)` from bounded equivalence over
arbitrary initial rows; scaling from a least-squares fit over at least four
octaves in `{2^10 ... 2^20}` with `R^2` reported; the sealed 64 consulted once
on the final population as pass/fail, never as a gradient; no space cap; the
claim gate needing `n_max >= 1024`, `alpha_hat < 1.9` with `R^2 >= 0.99` over
three consecutive octaves, an out-of-band `n`, and 64/64 sealed.

One amendment forced by §2.2. `n_max` is now measured on the GF(2)-projected
term, not on the field term, so it is the same instrument as arm 3 and the two
arms' `n_max` values are comparable. If the projection rejects a candidate, that
candidate has `n_max = 0` and dies, and the rejection reason is recorded in
`fatal_flaws` as `"non-boolean intermediate at <site>"` rather than as
inequivalence, because the two failures mean different things.

Target drift, flagged per `ARM4` §4. The brief states the target as `o(n)`,
which is Wolfram's Problem 3 proper. Arm 3 measures `alpha_hat < 2`, the weaker
variant. Any arm 4 number carries the same gap-stating sentence arm 3 does.

---

## 5. What AIR actually buys, since it is not nothing

Two things, and both are worth having on their own terms once they stop being
sold as a shortcut.

**A third-party-checkable claim.** The arithmetization in §3 plus a STARK
backend produces a proof that a claimed center-column value is the value rule 30
produces, checkable in polylog time by someone who does not trust this lab and
does not want to rerun `10^9` steps. `crosstalk-lab`'s sealed-commitment
tournament currently establishes trust by holding back cases. A proof object
establishes it without a holdout. That is a verification deliverable, it is
`O(n^2)` on the prover side and always will be, and it is the honest reason to
build `src/engines/rule30_air.rs`.

**A measurement instrument.** Additive FFT over `GF(2^k)` gives spectral support
of the trace rows directly, which is a sharper version of what `ARM4` §2 and §3
measured with Berlekamp-Massey and the Mobius transform. Sharper, and far more
expensive, and pointed at hypotheses those two probes already refuted. Build it
only if a specific new hypothesis needs it.

**The open edge, stated precisely so it is not overclaimed.** `ARM4` §2 excludes
the *linear / low-degree* shortcut: BM linear complexity of the center column
sits at the maximal-complexity ceiling on every prefix through 16384, reproduced
today (`uv run --with numpy python spectral_probe.py bm`, `L/(len/2)` between
0.9961 and 1.0312 across nine prefixes). That table does not exclude a nonlinear
or higher-degree shortcut. It excludes the one the brief proposes.

The only demonstrated reducibility anywhere in rule 30 remains left-permutive
inversion, `SEARCH-ARCH.md` §1.3, the Meier-Staffelbach 1991 line. It is already
a first-class primitive in the GF(2) grammar and it has no frequency-domain
analogue, because it is a per-cell algebraic solve rather than a global
transform. A pivot away from that grammar is a pivot away from the one piece of
known structure the field has.

---

## 6. Build order, cheapest disconfirming step first

Steps 1 and 2 are both cheap and both can kill the arm outright. Nothing below
step 3 is worth writing until both pass.

1. **Hand-write the §1.3 witnesses.** The pointwise one, and one that uses
   `Eval`/`Interp` non-trivially and is correct at `n = 16`. **Kill: no
   FFT-bearing correct program is hand-writable, so the transform primitives are
   decoration and the pivot has no content.** Cost: an afternoon with pen and a
   python model, no Rust.
2. **Term encoder plus GF(2) projection, per §2.3, checked against the
   `SEARCH-ARCH.md` §3.3 boolean driver at `n = 64`.** **Kill: the projection
   rejects the §1.3 witnesses, meaning the sorts are wrong.**
3. Additive-FFT implementation over `GF(2^k)`, Gao-Mateer or LCH basis, with the
   field-arithmetic crate's API confirmed through context7 against the workspace
   toolchain rather than from memory, and validated against a naive `O(N^2)`
   multipoint evaluation on random inputs. **Kill: no crate on the pinned
   toolchain provides a correct binary-field backend, and hand-rolling one is
   out of scope for a search-space experiment.**
4. `src/engines/rule30_air.rs`, width `2n+1`, per §3. Scoped as the verification
   deliverable from §5, not as a search component, and gated on someone wanting
   third-party-checkable claims.
5. Generator and evaluator over `ConceptDraft.mechanism`, reusing the
   S-expression serialisation and the fitness-axis mapping from
   `SEARCH-ARCH.md` §4 with its logged debt unchanged.
6. Run, under the §4 gate and the pre-registered kill condition.

**Pre-registration status: this arm is not pre-registered and must not run
until it is.** `PREREGISTRATION.md` needs a new arm 4 entry in the form the
existing arms use, with task, baseline, metric, strong-outcome and a kill
condition able to fire on a plausible negative, added before step 5 and not
after. The `ARM4` §4 note applies: "reject any algorithm that evaluates the
polynomial row-by-row" is malformed as a kill condition, because it fires on the
committed baseline rather than on a negative result, and removing the baseline
removes the measurement.

**Honest expected outcome.** §0.1, §0.2 and §0.4 are three independent
disconfirmations of the stated mechanism, two of them measured. The most likely
path through this document is that step 1 kills the arm in an afternoon, which
is the cheapest possible place for it to die and the reason step 1 is step 1.
