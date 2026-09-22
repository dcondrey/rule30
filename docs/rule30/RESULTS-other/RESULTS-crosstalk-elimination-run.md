# Crosstalk elimination run, 2026-08-27

## Purpose

This run tested whether Crosstalk's native idea evolution plus adversarial
orchestration could use the negative results in arms 3--5 as exclusion
constraints and produce one exact, falsifiable mechanism outside the closed
families.

The evidence pack contained the Rule 30 preregistration, arm-3 baseline,
frequency-domain and superposition negatives, the search architecture, the
superposition probe, an explicit elimination map, and the 2026 Nersissian and
Chan-Lopez/Martin-Ruiz adjacent work. The run used one bounded evolution
generation (six attempts, twelve proposer/critic call slots), then two
orchestration turns.

The native OpenAI route returned HTTP 429 and fell back to OpenRouter. DeepSeek
returned HTTP 402 and its fallback failed validation. The completed run used
OpenRouter `o3-mini` for variation and Mistral `codestral-latest` for criticism
and orchestration.

## Evolution result: no candidate survives

Five candidates remained on the reported Pareto frontier. They are not five
mechanisms. All propose the same object:

1. partition time or error events into dyadic blocks;
2. assume a direct parity query or an `O(1)` merge summary for each block;
3. combine block summaries along the binary expansion of `n`.

None supplies the required exact recurrence. Phrases such as "under an exact
composition law (derivable...)" and "uses an appropriate shift correction"
name the missing lemma instead of deriving it. Four proposals depend directly
on parity cancellation already measured false in ARM5. The nominal critic gave
all of them evidence scores of 6/10, feasibility 7--8/10, and no fatal flaw.

The correct evaluation is therefore: **zero surviving candidates**. The missing
lemma remains an exact composition law for either the Nersissian support-query
parity or a center-only multi-step observable whose state is `o(n)`. Without the
lemma there is no algorithm and no time recurrence to measure.

## Synthesis result: rejected

The final response invented an undefined `candidate_algo`, assumed both its
correctness and an `n^1.9` time bound as Lean axioms, and used `sorry`. It also
misread the arm-3 measured `1.9676` exponent of ordinary bit-packed forward
simulation as support for a dyadic algorithm that was never implemented.

Crosstalk's stored formal-verification record correctly says:

```text
PolicyViolation: untrusted proof placeholder rejected: sorry
```

Nevertheless, the turn was recorded with outcome `Compiled`, the headless CLI
printed the rejected artifact as its result, and the investigation audit said
`PASS` with zero verified claims and 0.0% verification coverage. The separate
offline bundle verifier then failed at retained transcript index 2. These are
application defects; neither the final response nor the bundle's `PASS` label
is scientific evidence.

## Productive use of the application

For this problem, Crosstalk is useful only when model output is treated as an
untrusted proposal queue and every proposal is routed to a domain-specific
objective gate before it can survive or enter synthesis. The main CLI does not
yet schedule that bridge automatically.

One residual interpretation was precise enough to test without assuming its
conclusion: a fixed-state binary-digit query, equivalently a small finite
2-kernel, and its bounded-rank linear version. `ARM6-binary-kernel.md` records
the preregistered probe. Both kill conditions fire: 8191 cumulative residuals
are distinguished through depth 12 and the depth-9 residual matrix reaches
full GF(2) row rank 512. This closes the small fixed-state and small fixed-rank
versions while preserving the finite-data boundary.

The run therefore advanced the search only after its model conclusions were
discarded and its residual mechanism was translated into a deterministic
falsification test.

## Remediation implemented after the run

The defects exposed here now have regression coverage. Post-write verification
is transactional: any failed checker marks the turn `VerificationFailed`,
restores the previous in-memory and on-disk artifacts, lowers convergence,
re-signs the finalized turn, rebuilds the transcript chain, and checkpoints the
corrected state. Headless output no longer selects a rejected turn as its final
response.

Native evolution now accepts repeatable `--evolve-constraint` and
`--evolve-exclusion` inputs. New candidates must provide an executable contract
containing the exact relation, composition rule, complexity argument, objective
test, and an explicit distinction from every exclusion. Structural duplicate
memory suppresses cosmetic variants, and generation reports identify why
candidates were rejected. See `CROSSTALK-RUNBOOK.md` for the next command.

The evidence-integrity audit remains an integrity check. A separate scientific
release assessment now stays `NOT ESTABLISHED` when there are no explicit,
evidence-linked, objectively verified facts or inferences. Domain-specific
objective evaluators still have to be selected and run; model fitness and
contract admission do not substitute for that step.
