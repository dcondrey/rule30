# Rule 30 — pre-registration

Written before any tournament run. Records the target, the baselines, the
metrics, the strong outcome, and the kill condition for each of Wolfram's three
Rule 30 Prize problems, plus the reason two of the three get no compute.

## Problem statements (verbatim, rule30prize.org)

1. "Does the center column always remain non-periodic?"
2. "Does each color of cell occur on average equally often in the center column?"
3. "Does computing the nth cell of the center column require at least O(n) computational effort?"

Problem 3's fine print, from Wolfram's 2019 announcement: the model of
computation is a Turing machine receiving the digit representation of `n`; a
solution must output the correct nth center-column value for all `n` with
`lim sup (steps / n)` finite as `n -> infinity`. Wolfram adds that "the choice
of O(n) computational effort is somewhat arbitrary; another version of this
problem could ask for O(n^alpha) for any alpha < 2."

## Ground truth

`experiments/rule30/center_column.py` generates the center column bit-parallel
(`new = (row<<1) ^ (row | (row>>1))`, whole row as one integer). Its first 30
terms match OEIS A051023 exactly, fetched from the OEIS API, not from memory.
Orientation is not a degree of freedom: rule 86 is the mirror of rule 30 and a
lone-1 initial condition is symmetric, so both orientations give the same
center column (verified empirically, and noted on the OEIS page by Karttunen).

## Arm 1 — non-periodicity: NOT RUN

No finite computation distinguishes "non-periodic" from "period longer than
anything computed." Settling it needs a theorem, and the strongest known
adjacent result is already Jen 1986 (no two columns can both become periodic;
J. Stat. Phys. 43, 219-242). Pointing an evolutionary search or an LLM debate
at a Lean proof of an open problem yields non-compiling artifacts or
trivialities relabelled as lemmas. "Find a lemma" is not a pre-registerable
target, so this arm gets no compute.

Permitted use of the formal-checking surface: formalize Jen's theorem in Lean 4
and label the result **validation of the proof pipeline**, never discovery.

## Arm 2 — color frequency: NOT RUN as discovery

The theoretical pathway here is already complete, and it lands one measure-zero
step short. Rule 30 is left-permutive, hence surjective, and a surjective CA
preserves the uniform Bernoulli measure (Hedlund 1969); left-permutivity gives
the stronger statement that rule 30 is *ergodic* with respect to it. So for
almost every initial configuration the center column already has density
exactly 1/2. Problem 2 survives only because the lone-1 initial condition is a
single measure-zero point, and an ergodic theorem says nothing about a
measure-zero orbit. Searching for the invariant measure is therefore searching
for something known.

Asymptotic density is also not decidable from any finite prefix. The column is
already published to 10^9 bits with a measured 1:0 ratio of 1.0001001570154626
(1.000399119632349 at 10^8, 1.003076725850907 at 10^6). Our own generator
reproduces the trend (1.003927698289 at 10^5), which is a check that the
pipeline is correct and nothing more. Recomputing it is pipeline validation,
one line in a writeup, not a run.

## Arm 3 — computational effort: THE ONLY ARM THAT RUNS

This is the one problem with a machine-checkable, falsifiable target, because a
negative answer is an *exhibited algorithm* rather than a theorem.

**Prior art check.** The naive upper bound is O(n^2) cell updates. No
sub-quadratic algorithm for the center column is known; the most recent
adjacent work (Chan-Lopez & Martin-Ruiz, arXiv:2604.00165, 2026) gives an
algebraic account of rule 30's left-permutive symmetry breaking and explicitly
claims no complexity improvement. Meier & Staffelbach 1991's stream-cipher
attack is the only existing demonstration that partial-information shortcuts
into rule 30 exist at all; it does not yield center-column cells.

**Task.** A WASM module exporting one `i64 -> i64` function returning bit `n`
of A051023.

**Baseline.** Naive bit-parallel forward simulation, committed as the baseline
artifact of the tournament.

**Metric.** `fuel_consumed`, wasmtime's deterministic step counter. This is a
machine-independent effort proxy and is far closer to Wolfram's Turing-machine
step count than wall clock. `elapsed_ms` is recorded but is not a decision
metric.

**Design.** Separate sealed runs at n-bands (10^3, 10^4, 10^5, 10^6), each with
its own committed hidden test set. Fit log(fuel) against log(n) across bands to
estimate the scaling exponent `alpha_hat`.

**Strong outcome.** A correct candidate with `alpha_hat < 1.9` sustained across
at least three bands, and holding on a fresh hidden test set at a band the
candidate never saw.

**Kill condition.** After the budgeted generations, no candidate beats the
baseline's `alpha_hat` on out-of-band `n`. This fires on a plausible negative
and it is the expected outcome. Reported as a negative result: LLM proposal
plus evolutionary search over WASM found no sub-quadratic shortcut under this
budget. That is publishable and it is the honest default.

**Prize gap, stated up front.** `alpha_hat < 2` answers the weaker variant
Wolfram names in the announcement. It does **not** win Problem 3, which needs
`o(n)`. Any result from this arm is labelled a speedup result with the gap to
the prize threshold stated in the same sentence as the number.

### Two ways this arm silently fakes a win, and the defenses

**Table lookup.** The center column is public to 10^9 bits. A candidate can
embed it. The current lab cap `MAX_WASM_BYTES = 32 MiB` admits ~2.7x10^8
tabulated bits, which is more than enough to pass any band below 10^8.
Defenses, all required together: cap the module at 64 KiB via the challenge
file's `max_candidate_bytes`; place decision bands
at n >= 10^6; and score `alpha_hat` on out-of-band `n`, where a table covering
the fitted bands collapses to a wrong answer rather than a fast one.

**Chance floor.** The output is one bit, so a coin flip passes a single hidden
case half the time and `all_cases_correct` over k cases has a chance floor of
2^-k. Five hidden cases means a guesser wins one run in 32. Minimum 64 hidden
cases per band.

### What crosstalk actually contributes here

Models propose mechanisms (left-permutivity, backward solving in the
Meier-Staffelbach style, algebraic or Boolean-circuit decomposition); those get
compiled to WASM; the sealed two-worker tournament with committed hidden tests
disposes of them. Model agreement decides nothing. The evaluator does.
