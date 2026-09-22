# Fringe-framework attack on P1/P2/P3: four arms assessed

`deg f_t = 2t-1` was
accepted as given and never re-verified; zero compute spent on it.

## Verdict up front

**No arm produced a proof.  `ADVANCED_PROOF_DRAFT.md` is not written.**
Three arms fail at their premise, and each failure was established by a cheap
decisive test rather than asserted.  Arm 4's stated conclusion is false, but
its computation is legitimate under a different framing and was run: the
first exact algebraic-immunity values for the Rule 30 center-bit function.

## The filter that kills every "complexity grows" argument (arms 1 and 3)

`PATH.md` section 0: an argument that also applies to Rule 90 proves nothing.
Rule 90's lone-seed pattern has unbounded structural complexity (Sierpinski,
nested at every scale, defect structures growing without bound), and its
center column **is** eventually periodic - identically 0 for all `t >= 1`.

So for **any** complexity measure `B(t)` defined on the space-time pattern,
"`B(t) -> infinity` monotonically" cannot imply center-column aperiodicity,
because the implication is false for Rule 90.  This kills arm 3 (braid
length) and the "maximal scrambling" half of arm 1 outright, independent of
whether the measures are well defined.

## Arm 1 (OTOC / spectral form factor): premise is false

RMT spectral statistics (GUE/GOE spacing) and the SFF are defined for
unitary or Hermitian evolution.  **Rule 30 is not invertible**, so no unitary
evolution operator exists.  Measured directly on cyclic lattices:

| N | states | distinct images | bijective | max preimages |
|---|---:|---:|---|---:|
| 3 | 8 | 5 | No | 3 |
| 5 | 32 | 26 | No | 2 |
| 8 | 256 | 223 | No | 2 |
| 12 | 4096 | 3816 | No | 3 |
| 14 | 16384 | 15571 | No | 2 |

Non-bijective at **every** `N` from 3 to 14.  The evolution matrix is a
0/1 non-permutation matrix; its spectrum is dominated by the nilpotent part
(the transient tree feeding the cycles) plus roots of unity from the cycles.
That is not a random-matrix ensemble and Wigner-Dyson spacing is not the
prediction; no "spectral chaos proof" can be built on it.

Separately, the classical OTOC of a deterministic CA **is** damage spreading,
which is already measured and published for Rule 30: NKS p.949 gives the
difference-pattern left edge at ~0.2428 cells/step executing "essentially a
random walk", with rightward speed exactly 1 by left permutivity.  Computing
it as an "OTOC Lyapunov exponent" renames a known measurement.  And a
Lieb-Robinson-style bound is a statement about information *speed*, which
bounds nothing about the equidistribution or the cost of one specific column.

## Arm 2 (2-adic / Mahler): unique ergodicity is provably false

Partial credit on the setup: the map is continuous on `Z_2` (each output
digit depends on finitely many input digits), so a Mahler expansion does
exist.  It is **not** 1-Lipschitz / not a T-function, because the new cell at
`i` depends on cell `i+1`, a higher-index digit; the Klimov-Shamir T-function
machinery therefore does not apply.

The hypothesis itself is false in one line.  Haar measure on `Z_2` is the
uniform Bernoulli measure.  Rule 30 has the all-zeros fixed point, so
`delta_0` is invariant; uniform Bernoulli is also invariant (Hedlund: Rule 30
is surjective, `<= 4` preimages, cf. Taati arXiv:1505.06464 section 2.4).
**Two distinct invariant measures exist, so the system is not uniquely
ergodic**, under Haar or anything else.  Unique ergodicity cannot be proved
because it is false.

What remains after the false part is removed is exactly the known statement
(uniform Bernoulli is invariant, hence density 1/2 for almost every initial
configuration) and exactly the known gap (`PREREGISTRATION.md` Arm 2: the
lone seed is a single measure-zero point).  This is route R8 in different
clothing and does not cross the gap.

## Arm 3 (braid group): no braid word exists

Braid group `B_n` requires `n` strands that persist and permute; a braid word
is a sequence of generator crossings on a **fixed** strand count.  Rule 30
defects are not conserved: they merge and annihilate, which is forced by
non-invertibility (measured above - up to 3 preimages, so distinct histories
converge).  A world-line diagram with merging strands is not a braid, and no
Artin generator word `w(t)` is defined for it.

Even granting a defect-count proxy, the Rule 90 filter above closes it.

## Arm 4 (algebraic immunity): conclusion false, measurement real and new

**The AC0 claim is false.**  Algebraic immunity does not lower-bound AC0
size or depth, and degree does not either.  Clean counterexample, verified in
code: `AND_n` has F2-degree `n` (maximal) and a one-gate depth-2 AC0 circuit;
its algebraic immunity is **1** (`(1+x_0)` annihilates it - confirmed by the
solver at `n=6`).  Degree, AI and AC0 hardness are three different things.
Smolensky needs *approximate* degree / correlation bounds, not exact degree
or AI.  This is the same error already refuted in
`p3_circuit_attack/P3_ASSESSMENT.md`, arriving through a different door.

The category error also stands: `f_t` has `n = 2t+1` variables, so an
`Omega(t)` bound is `Omega(n)` on `n` variables - the trivial regime - and
Problem 3 fixes the input to the lone seed, where non-uniform circuit
measures are identically zero.

**What was worth computing.**  AI is the right notion for algebraic attacks
on Rule 30 *as a stream cipher*, which is the Meier-Staffelbach EUROCRYPT '91
line.  Exact values, computed by F2 kernel search over all monomials of
degree `<= d` on the support (`algebraic_immunity.py`):

| t | n = 2t+1 | \|supp f_t\| | **AI(f_t)** | bound ceil(n/2) | deg f_t = 2t-1 |
|---|---:|---:|---:|---:|---:|
| 3 | 7 | 64 | **3** | 4 | 5 |
| 4 | 9 | 256 | **3** | 5 | 7 |
| 5 | 11 | 1024 | **4** | 6 | 9 |
| 6 | 13 | 4096 | **5** | 7 | 11 |
| 7 | 15 | 16384 | **6** | 8 | 13 |
| 8 | 17 | 65536 | **6** | 9 | 15 |

Two facts worth recording, both honest and neither a prize result:

1. `|supp f_t| = 2^(n-1)` exactly at every `t`: `f_t` is **balanced**.  This
   is the expected consequence of left permutivity (each column word has
   exactly `2^(t-1)` generating light-cone words), so it is a pipeline
   validation, not a discovery.
2. **AI grows, but strictly below the `ceil(n/2)` bound and below degree**:
   observed 3, 3, 4, 5, 6, 6 against bounds 4, 5, 6, 7, 8, 9.  Fitting
   crudely, `AI ~ 0.75t`.  So `f_t` is *not* AI-optimal, i.e. it is weaker
   against algebraic attack than a generic balanced function of the same
   arity.  That is a small, concrete, citable measurement in the
   Meier-Staffelbach citation graph, and it is the only new thing this round
   produced.

Cost note: `t=8` took 485 s; the method is exponential in `n` (needs the full
`2^n` truth table), so `t=9,10` are out of reach without a smarter annihilator
search.  The requested range `t in [3,10]` was therefore not completed, and
the table says so rather than extrapolating.

## Files

* `experiments/rule30/p_fringe_attack/algebraic_immunity.py` - exact AI
  solver plus the `AND_n` sanity check.
* This document.

Reproduce: `uv run --no-project python algebraic_immunity.py 5` (seconds);
`t=6..8` via `algebraic_immunity(t)` directly.
