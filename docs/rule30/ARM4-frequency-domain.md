# Arm 4 — AIR / frequency-domain shortcut: phase-0 probe result and the
# conditional architecture

Status: **phase 0 ran, all three measurements disconfirm the premise.** Phase 1
(the AIR module and the additive-FFT hookup) is gated on phase 0 and is not
built. This document records the probe, the corrections to the proposal as
stated, and the architecture that would be written if the gate ever opens.

Probe code: `experiments/rule30/spectral_probe.py`. It reuses the generator in
`center_column.py`, already validated against OEIS A051023 per
`PREREGISTRATION.md`.

## 0 — The proposal, and the four things wrong with it before any code

**Proposal.** Arithmetize the rule 30 light cone as a STARK AIR over a binary
extension field, FFT the trace into the frequency domain, and search for a
low-degree extension mapping the low-entropy right boundary directly to the
center-column coefficient, evaluating the center node without the intermediate
algebraic steps, in `o(n)`.

**(a) STARK sublinearity is a verifier property, not a prover property.** In a
STARK the prover computes the entire trace — here the full `O(n^2)` light cone —
commits to it, and the verifier checks a polylogarithmic number of openings. FRI
compresses *verification*. This lab has no untrusted prover and no verifier; it
is the party that wants the bit. There is nobody to receive a proof from.
"Hijack trace compression to evaluate without computing the intermediate steps"
asks the prover side to inherit the verifier's cost bound. That is not an open
question, it is a category error, and no amount of field or transform choice
changes it.

**(b) Low constraint degree and no intermediate rows are the two ends of one
lever.** The local rule over GF(2) is

    f(L, C, R) = L + C + R + C*R

degree 2. An AIR keeps that degree 2 *by* carrying one trace row per time step;
the transition constraint only ever relates row `t` to row `t+1`. Eliminating
intermediate rows means composing transitions, and each composition squares the
degree, so the composed map to row `n` has degree `2^n`. You may have degree 2
with `n` rows, or one row with degree `2^n`. There is no configuration with
both, and the whole low-degree machinery is defined on the first.

**(c) An FFT is a change of basis, so it is linear.** The `L + C + R` part
transforms cleanly. The `C*R` term becomes a convolution in the transform domain
and spreads spectrum rather than sparsifying it. A transform does not diagonalize
a nonlinear map. Additive FFT over binary extension fields is real machinery
(Gao-Mateer / LCH, as used by binius) and would compile, but it does not do the
job asked of it.

**(d) The boundary orientation is backwards, and the underlying intuition is
inverted.** See §1.

## 1 — Which boundary is ordered, and why it constrains nothing

Under the convention in `center_column.py` (`new = (row<<1) ^ (row | (row>>1))`,
position increasing rightward), the first 20 rows from a lone 1:

```
  0 ....................#....................
  1 ...................###...................
  2 ..................##..#..................
  3 .................##.####.................
  4 ................##..#...#................
  5 ...............##.####.###...............
  6 ..............##..#....#..#..............
  7 .............##.####..######.............
  8 ............##..#...###.....#............
  9 ...........##.####.##..#...###...........
 10 ..........##..#....#.####.##..#..........
```

The regular striping is on the **left**. The right side is the chaotic one. That
is the standard picture and it is the opposite of the proposal's premise. Rule 30
is left-permutive, so information propagates rightward; the ordered region is the
side information leaves, not the side it arrives at.

Quantified rather than eyeballed. GF(2) linear complexity `L` of the diagonal at
depth `d` in from each light-cone edge, over 4096 rows (`L/(N/2) = 1.0` is the
maximal-complexity ceiling, i.e. no linear recurrence shorter than the sequence
itself):

| depth d | left L | left/ceiling | right L | right/ceiling |
|---|---|---|---|---|
| 0 | 1 | 0.0005 | 1 | 0.0005 |
| 5 | 4 | 0.0020 | 8 | 0.0039 |
| 10 | 9 | 0.0044 | 59 | 0.0288 |
| 15 | 16 | 0.0078 | 65 | 0.0317 |
| 20 | 26 | 0.0127 | 256 | 0.1250 |
| 25 | 31 | 0.0151 | 513 | 0.2505 |
| 29 | 35 | 0.0171 | 2049 | **1.0005** |
| 31 | 39 | 0.0190 | 2049 | **1.0005** |

The right boundary saturates to maximal linear complexity by depth 29. The left
boundary is still at `L ~ d` at depth 31 — diagonal `d` obeys a linear recurrence
of order roughly `d`.

**That last fact is the load-bearing one, and it is the reason the hypothesis
fails independently of everything in §0.** The ordered boundary is ordered
*because it is decoupled from the interior*, not because it encodes it. Diagonal
`d` carries about `d` bits of state. Reaching the center bit at step `n` means
reaching depth `d = n` in from the edge, by which point the cheap region is long
gone and the complexity has saturated. A boundary whose information content grows
as `d` cannot "severely constrain the roots" of anything at depth `n`. The
proposal reads the low entropy of the ordered side as evidence that it determines
the center cheaply; it is evidence of the opposite.

## 2 — Linear complexity of the center column itself

Berlekamp-Massey over GF(2) on prefixes of A051023:

| length | L | L/(length/2) |
|---|---|---|
| 64 | 33 | 1.0312 |
| 256 | 128 | 1.0000 |
| 1024 | 513 | 1.0020 |
| 4096 | 2049 | 1.0005 |
| 16384 | 8192 | 1.0000 |

Exactly the maximal-complexity profile of a random sequence, at every prefix
through 16384. A sparse frequency-domain representation, or a low-degree
univariate extension over an evaluation domain, is a linear-algebraic statement
about the sequence and would show up here as sub-maximal complexity. It does not.
This is the specific hypothesis of the proposal — "a low-degree extension mapping
the boundary to the center-column coefficient" — and this table is its
disconfirmation. It does not exclude a nonlinear or higher-degree shortcut; it
excludes the one that was proposed. Consistent with the Meier-Staffelbach 1991
stream-cipher line, but measured here rather than cited.

## 3 — Algebraic degree of the center bit

Center bit at step `t` as a boolean function of the `2t+1` row-0 cells in its
light cone, via Mobius transform to ANF:

| t | vars | ANF degree | ceiling | terms | density |
|---|---|---|---|---|---|
| 1 | 3 | 2 | 3 | 4 | 0.500 |
| 3 | 7 | 5 | 7 | 30 | 0.234 |
| 5 | 11 | 9 | 11 | 346 | 0.169 |
| 7 | 15 | 13 | 15 | 4852 | 0.148 |
| 9 | 19 | 17 | 19 | 79192 | 0.151 |
| 10 | 21 | 19 | 21 | 324572 | 0.155 |

Degree is exactly `2t-1`, two below the ceiling, at every `t` measured. Density
plateaus near 0.15 rather than decaying. "Low-degree extension" is the phrase the
proposal turns on; the measured degree grows linearly in `t` and sits at the
ceiling minus a constant.

**Kill condition, as it would have been pre-registered:** spectral/ANF support
stays above 5% dense and linear complexity stays above `L/4` through the measured
range. Both fired, by a wide margin, on the first run. Phase 1 does not open.

## 4 — Corrections to the three code drafts

Recorded because the errors are load-bearing, not stylistic.

**AIR draft.** `winter_math::fields::f64::BaseElement` is the Goldilocks prime
field `p = 2^64 - 2^32 + 1`, not GF(2), and the comment deferring "use a binary
extension field in production" defers the thing that makes the arithmetic
correct. Over a prime field, cells need explicit booleanity constraints
(`x^2 - x = 0`) and XOR is `a + b - 2ab`, not `a + b`; `L + C + R + C*R` is
simply not rule 30 there. Winterfell has no binary-field backend, so the module
as drafted cannot be made correct by swapping a type alias. Separately, and
fatally on its own terms: a 3-column sliding-window trace cannot express rule 30.
Each cell's successor needs its own neighbours, so the trace must be the full
`2n+1`-wide light cone. With `result[0] = next_row[1] - poly` as the only
constraint, columns 0 and 2 are unconstrained and any trace satisfies the AIR.

**Z3 equivalence draft.** It checks a candidate against one step of rule 30 over
three boolean variables. That domain has 8 points; a truth table settles it in 8
evaluations and an SMT solver buys nothing. More to the point, the object being
searched for is the center bit at step `n`, which is not a function of `(L, C, R)`
at all, so passing this check says nothing about the candidate.

**Z3 induction draft.** `get_left_neighbor(&ai_k_steps)` applied to a single
`Bool` is where the formulation collapses: a scalar has no neighbours. Stating
the inductive step honestly requires `S(k, X)` to return the whole row, whose
width grows with `k`, so the induction hypothesis quantifies over an
unbounded-width object. That needs quantifiers over arrays or uninterpreted
functions, which is undecidable in general and returns `unknown`, not
milliseconds. The claimed "logic depth 2, constant time regardless of `n`" holds
only for a candidate already expressible as a quantifier-free formula in a
decidable theory with symbolic `n` — which is most of the problem, assumed
solved.

Two further points on that draft, both about the measurement rather than the
solver:

- "Fuel stays flat, so `alpha -> 0`" describes `solve(n) = 1` exactly. That
  candidate was already submitted in run 1: 406 bytes, flat fuel, accuracy
  0.53125, rejected on `all_cases_correct`. Flat fuel is not evidence of
  anything; correctness at 64 hidden cases per band is the binding constraint and
  already is.
- `alpha < 1.95` as the breakthrough threshold would have fired on run 1. The
  bit-parallel baseline fit `alpha_hat = 1.9676`, and `RESULTS-arm3-run1.md`
  established that as small-`n` loop overhead by refitting on the two largest
  points (1.985, climbing toward 2). `PREREGISTRATION.md` sets `alpha_hat < 1.9`
  sustained across three bands *plus* a fresh out-of-band hidden set. That stands.

**The proposed kill condition is malformed and was not adopted.** "Reject any
algorithm that evaluates the polynomial row-by-row" cannot fire on a negative
result — it fires on the baseline. `PREREGISTRATION.md` commits naive
bit-parallel forward simulation as the baseline artifact, and `alpha_hat` is
defined against it. Removing it removes the measurement.

**Target drift, flagged per the prize-gap discipline.** The proposal states the
target as `o(n)`, which is Wolfram's Problem 3 proper. Arm 3 measures against
`alpha_hat < 2`, the weaker variant. Arm 4 does not get to quietly reset that
threshold in the favourable direction; any arm 4 number carries the same
gap-stating sentence arm 3 does.

## 5 — Phase 1, drafted but not built

Written down so the interface is on record, conditional on a phase-0 gate that
did not open.

- `src/engines/rule30_air.rs` — the light cone as an AIR over `GF(2^128)` via a
  binary-field crate confirmed to build on the workspace toolchain (edition 2024,
  rust 1.91) with its API checked through context7, not from memory. Trace width
  `2n+1`, one row per step, one degree-2 transition constraint per interior
  column, boundary assertions pinning the lone-1 row 0. This is a correct
  arithmetization and it is `O(n^2)` cells; it buys a proof object, not a
  shortcut.
- Additive FFT (Gao-Mateer / LCH) over that field to move rows between
  coefficient and evaluation bases. Useful for measuring spectral support, which
  is what §2 and §3 already did more cheaply.
- Synthesizer target and kill condition would go into `PREREGISTRATION.md` as a
  new arm before any run, in the form the existing arms use.

The honest summary of arm 4 as it stands: the frequency-domain shortcut
hypothesis was tested at the cheapest level that can refute it, and it was
refuted on all three measurements. That is a negative result, it is the expected
one, and it cost three python probes instead of an AIR backend.
