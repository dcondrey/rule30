# Crosstalk Rule 30 elimination runbook

The useful role for Crosstalk here is not to vote a closed form into existence. It is to maintain a shrinking, auditable search space: each failed mechanism becomes a structural exclusion, every replacement must supply the exact missing composition law, and checker or probe failures remain failures.

From the repository root, build and run a fresh bounded search:

```bash
cargo run --release -- \
  --headless \
  --headless-format json \
  --bundle-dir ./runs/rule30-next \
  --task "Find an exact algorithm for the Rule 30 center cell s_n(0) from n in time polynomial in log n. Do not simulate a linear-width light cone. Return the state representation, exact identity, composition rule, complexity proof obligation, and a deterministic falsification probe." \
  --workspace . \
  --files docs/rule30/PREREGISTRATION.md docs/rule30/ARM5-superposition.md docs/rule30/ARM6-binary-kernel.md docs/rule30/RESULTS-crosstalk-elimination-run.md docs/rule30/RESULTS-crosstalk-elimination-run2.md docs/rule30/RESULTS-crosstalk-elimination-run3.md \
  --evolve-generations 3 \
  --evolve-population 8 \
  --evolve-concurrency 4 \
  --evolve-max-model-calls 48 \
  --evolve-constraint "the identity must be exact for every n, not a fit to a bounded prefix" \
  --evolve-constraint "the composition rule and its state-size bound must imply poly(log n) work" \
  --evolve-constraint "the objective test must compare against bit-parallel ground truth on preregistered held-out n" \
  --evolve-exclusion "row-parity cancellation;approximately one half of rows survive;survival exponent Theta(n);no favorable dyadic band" \
  --evolve-exclusion "finite 2-kernel automaton;all residual prefixes distinct through depth 12;GF(2) residual rank 512 at depth 9" \
  --evolve-exclusion "left-permutive affine boundary map;polylogarithmic claim assumes an unproved short period in the time-varying maps" \
  --evolve-exclusion "inverse-diagonal transfer matrix;exact only for the Rule 150 linear component;full Rule 30 update remains nonlinear" \
  --evolve-exclusion "carry-chain transfer matrix;exactness conditional on an undefined LEMMA_GATE predicate" \
  --evolve-exclusion "truncated carry-polynomial matrix;constant-term transfer predicts one for every n;first mismatch at n=2;exact truncation and factorization unproved" \
  --auto
```

The semicolon-separated phrases in each `--evolve-exclusion` are structural features. Crosstalk gives each exclusion a stable ID, requires every new candidate contract to explain its difference from every ID, rejects high-overlap contracts deterministically, and carries rejected structural fingerprints into later generations.

The call-slot scheduler gives every requested generation a fair share of the
remaining budget and carries unused slots forward. Invalid evaluator output is
also negative knowledge: when enough candidate context exists, its title,
structural fingerprint, and failure reason enter the rejection ledger rather
than disappearing between generations.

Inspect these bundle/session artifacts before spending more compute:

- `evolution/generation-reports.json`: rejection counts by reason, including missing contracts and structural duplicates.
- `evolution/checkpoint.json`: exclusions, rejected structural memory, critic fatal flaws and rejection scores, full lineage, and any later objective feedback. When a generation has no survivor, these failure reasons become the next generation's directive.
- `evolution/native-candidates.json`: surviving proposals. `objectively_verified: false` is expected until a real proof, test, simulation, or benchmark result is attached.
- the headless `scientific_release` field: `NOT ESTABLISHED` is the correct state until explicit substantive claims have accepting objective verification.

Negative results narrow mechanism families, not the set of all possible algorithms. Elimination becomes a proof of impossibility only when the excluded families are shown to exhaust a formally defined search space. Until then, use the surviving contracts to choose the next cheap discriminator; do not infer that the last remaining model proposal is correct.

## Orthogonal ARM7 run

The dyadic spacetime measurements in `ARM7-dyadic-spacetime-grammar.md` support
a narrower unconventional search.  Add that file and its executable probes to
the context, change the task from unrestricted closed-form search to exact tile
composition, and add these exclusions:

```text
generic recompression;second pass gives no Rule 30 advantage;no composition law
simple axial periodicity;no repeated complete horizontal or vertical strips at tile scales 8 through 64
dihedral symmetry quotient;no tile vocabulary reduction at scales 8 through 64
decorative 3D projection;third axis must be reversible and supply an exact composition operation
empirical subquadratic compression;measured exponents remain superlinear;does not imply polylogarithmic evaluation
```

The candidate contract in ARM7 is the acceptance gate.  In particular, a
candidate that merely names tensor networks, renormalization, wavelets, or
grammar compression without defining its state and composition operation is
malformed, not a surviving hypothesis.

## Width-two to width-one periodicity bridge

`RESULTS-periodicity-bridge.md` records a separate proof-first search for Prize
Problem 1.  Feed its exact defect identity and executable counterexamples into
Crosstalk; do not mix this task with the algorithm tournament above.  The
useful target is a universally quantified lemma, not another long prefix:

```bash
cargo run --release -- \
  --headless \
  --headless-format json \
  --bundle-dir ./runs/rule30-periodicity-bridge \
  --task "Derive a period-independent contradiction from an eventually periodic Rule 30 lone-seed center. Every candidate must state quantified variables, an exact lemma, its proof mechanism, and a bounded falsifier. Return no theorem if the bridge remains missing." \
  --workspace . \
  --files docs/rule30/RESULTS-periodicity-bridge.md experiments/rule30/periodicity_bridge_probe.py \
  --evolve-generations 2 \
  --evolve-population 6 \
  --evolve-concurrency 2 \
  --evolve-max-model-calls 20 \
  --max-model-calls 24 \
  --max-output-tokens 60000 \
  --evolve-constraint "the claim must quantify every period p and all sufficiently late times, not a finite prefix" \
  --evolve-constraint "the proof must use a lone-seed orbit property absent from the Rule 90 control" \
  --evolve-constraint "the candidate must provide an executable bounded falsifier before any proof attempt" \
  --evolve-exclusion "generic width-one expansivity;Rule 90 center is eventually constant;Kopra width-two theorem does not extend" \
  --evolve-exclusion "finite-delay neighbor reconstruction;Rule 30 has center-agreement runs with adjacent defects;Rule 90 has an infinite run" \
  --evolve-exclusion "generic center-trace injectivity;seed and seed-plus-right-neighbor have the same center trace;moving defect escapes right" \
  --evolve-exclusion "doubling separation witness;s(p,0) differs from s(2p,0);first counterexample p=4" \
  --models MODEL_A MODEL_B
```

Replace `MODEL_A MODEL_B` deliberately.  `--auto` may select more providers
than this tightly bounded proof task needs.  Model survival is only permission
to implement its falsifier; it is not mathematical evidence and does not open
the Modal gate.

## Inverse-trace continuation arm

`RESULTS-inverse-trace.md` rotates the periodic-center hypothesis into a
unique forced left half. This is a new mechanism relative to the time-shift
defect run, but the exact reconstruction alone is only a reformulation. A
bounded follow-up should ask specifically for a uniform obstruction to an
eventually-zero reconstructed tail and inherit the earlier rejection ledger:

```text
task: Derive a period-uniform obstruction showing that the Rule 30 lone-seed
      periodic inverse trace cannot reproduce its finite left half.
required object: a closed transition state, exact update, quantified lemma,
                 proof mechanism, and executable bounded falsifier.
control: Rule 90 at T=1,p=1 must retain its finite reconstructed tail.
exclusion: first outside cell is always one; false at Rule 30 T=4,p=1.
exclusion: inverse reconstruction itself proves nonperiodicity; it is a
           bijective re-encoding until a uniform tail obstruction is supplied.
exclusion: periodic OR-mask contracts all right-trace defects; a defect at a
           center-zero phase crosses the mask and its earliest time then moves
           one step earlier through every further reconstructed left column.
```

Do not rerun the broader periodicity prompt. Include
`experiments/rule30/inverse_trace_probe.py` and this arm's result file, and
reject any candidate whose alleged finite state still depends on an omitted
column or a prefix growing with `T` or `p`.
