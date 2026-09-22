# Evolutionary search on the P1 rank-zero separator

Date: 2026-09-01

Status: **OPENEVOLVE AND A BIT-LEVEL GA WERE RUN AGAINST AN INDEPENDENT EXACT
ZERO-TAIL VERIFIER.  THE GA REPRODUCES THE KNOWN `T=23` OPTIMUM AND IMPROVES
SEVERAL LARGE-CUTOFF WITNESSES, BUT NO CANDIDATE REACHES THE CONJECTURED
`2T+2` LIMIT.  THIS IS FINITE FALSIFIER DATA, NOT A PROOF OF THE RANK-ZERO
SEPARATOR OR OF PERIOD-TWO MORTALITY.**

The complete experiment is in `experiments/openevolve-p1-rank-zero/`.

## 1. Target and proof boundary

The rank descent now reduces the finite-Peel-rank obstruction to one exact
statement:

> No nonzero finite-support cut has a hard-core terminal-cone endpoint.

For a support cutoff `T`, triangular bijectivity lets a search propose a
hard-core endpoint prefix `e[0:T]`.  The verifier—not the evolved program—then
computes its unique inverse cut prefix, appends an exact zero ray, applies the
terminal cone, and reports the first endpoint symbol outside `{1,2}` or the
first `11`.

The finite census through `T=23` suggests

```text
hard-core survival < 2T+2.                              (1)
```

Crossing (1) at one cutoff would be a rigorous counterexample to that proposed
linear bound.  It would not produce an infinite hard-core endpoint.  Conversely,
failure to cross any finite list of cutoffs proves neither (1) nor the
rank-zero separator.

## 2. OpenEvolve generator search

The evolved object is a uniform `endpoint_prefix(T)` algorithm.  Imports,
I/O, reflection, unbounded loops, endpoint enumeration, and long literal
tables are rejected.  Small cutoffs are calibrated against the exhaustive
maxima; cutoffs `24,28,32,40,48,64,80,96` test extrapolation.

The 18-iteration search retained the alternating seed as its best program:

```python
return tuple(1 if index % 2 == 0 else 2 for index in range(cutoff))
```

Its headline metrics were:

```text
train extremality       0.9326
holdout extremality     0.7590
large-cutoff ratio      0.5093
worst large ratio       0.4923
2T+2 falsifiers         0
```

For example, its exact survivals at `T=48,64,80,96` are `51,70,81,96`.
The valid evolved variants did not improve the combined score.  The complete
program database, prompts, artifacts, checkpoints, and log are retained under
`openevolve_output_search/`; a credential scan found only the literal
`${OPENROUTER_API_KEY}` configuration placeholder.

## 3. Bit-level GA and exact witnesses

Code evolution is coarse on this landscape, so `ga_witness_search.py` mutates
individual hard-core phase slips.  Its genome never supplies a fitness value:
every score is recomputed by the exact inverse-cut/zero-tail/terminal-cone
pipeline.

The calibration run recovered survival `29` at `T=23`, equal to the exhaustive
optimum.  Selected extrapolation results are:

| cutoff `T` | best survival retained | proposed bound `2T+2` |
|---:|---:|---:|
| 32 | 39 | 66 |
| 43 | 55 | 88 |
| 48 | 56 | 98 |
| 64 | 73 | 130 |
| 96 | 107 | 194 |

The last value comes from a 35,961-evaluation search seeded by the `T=43`
phase-slip word.  None reaches (1).  `verify_results.py` independently replays
all 44 retained GA witnesses across the zero, constant-2, and constant-3 tail
corpora, plus the eight large-cutoff alternating witnesses, including the
literal endpoint and cut strings.

## 4. Structural lead and its negative control

The cutoff scan found conspicuous survival peaks near `T=7,18,43`.  Those
numbers tempt the continuation `96`, suggesting a dyadic morph of extremizers.
Two direct controls do not support the simplest version:

- forcing the exact `T=18` extremizer as the prefix of a `T=43` genome reaches
  only `51`, below the unconstrained search value `55`;
- repeating and mutating the `T=43` witness at `T=96` reaches `107`, with no
  corresponding jump toward `194`.

Thus the peak locations are useful adversarial data, but no nested extremizer
or substitution law has been found.  They must not be promoted to a recurrence.

## 5. Consequence

The hybrid search is useful for falsification and for constructing difficult
finite boundary collisions.  It did not discover a counterexample to (1), an
infinite survivor, or a uniform invariant.  Its strongest outcome is a
reproducible adversarial corpus for a future proof-bearing certificate.

The next evolution should therefore operate on a certificate whose soundness
is width-independent—for example, a checked rewrite or ranking on the exact
controlled-Peel recurrence.  Re-running numerical endpoint fitness at larger
cutoffs alone cannot close the theorem.

The subsequent first-infinite-tail reduction sharpens that target to the two
eventual cut tails `2^omega` and `3^omega`; their census and GA controls are in
`experiments/rule30/p1-period2-invariant/RESULTS-EVENTUAL-CONSTANT-TAIL.md`.

## 6. Reproduction

From `13-rule30/`:

```bash
./experiments/openevolve-p1-rank-zero/run_search.sh
uv run python experiments/openevolve-p1-rank-zero/ga_witness_search.py \
  --cutoffs 23 32 48 64 96 --population 96 --generations 120 \
  --seed 30047 --json experiments/openevolve-p1-rank-zero/ga_witness_results.json
uv run python experiments/openevolve-p1-rank-zero/verify_results.py
```

The recorded OpenEvolve checkpoints are the authoritative 18-iteration run.
The JSON files retain the deterministic GA seeds and every exact witness.
