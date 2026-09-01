# Rule 30: compact research index

Updated: 2026-09-01

Purpose: resume this project with the fewest tokens consistent with not
repeating work.  This file routes to authoritative sources; it is not itself a
source for publication claims.

## Current status

| Problem | Status | Best live edge |
|---|---|---|
| P1: center-column nonperiodicity | **OPEN** | R1's OR-specific zero-set obligation; within it, the period-two same-orbit rung |
| P2: limiting density `1/2` | **OPEN** | R8/orbit-closure route remains conditional; ensemble ergodicity does not reach the lone seed |
| P3: computational effort | **OPEN** | A genuine fixed-sequence work lower bound remains unproved; proof-complexity and finite circuit probes are bounded only |

Proved prize-adjacent results exclude eventually constant centers only:

- zero center tail: `RESULTS-zero-tail.md`;
- one center tail: `RESULTS-eventual-period.md` and
  `RESULTS-inverse-trace.md`.

No document proves a nonconstant-period exclusion, density convergence for the
lone seed, or a computational lower bound.

## Where every attempt is indexed

The register is split for historical reasons:

| Coverage | Canonical source |
|---|---|
| Ranked routes R1–R9 and internal rows 1–72 | `PATH.md` sections 4 and 7 |
| Frontier attack rows 73–90 | `experiments/overnight-arms/frontier_attack/FINDINGS.md` sections 1–7 |
| Later rows 91–93 | `PATH.md` section 7.1 |
| Period-two same-orbit continuation after row 90 | `experiments/rule30/p1-period2-invariant/README.md` |
| External literature/claim audit | `PATH.md` section 8 and the two `REFUTATION-*` files |

There is a historical row-number collision: `PATH.md` row 76 is the S-adic /
Morse–Hedlund subword attempt, while `FINDINGS.md` row 76 is the alternating
survivor-invariant attempt.  Always cite the file plus row number.

`overnight/CONTEXT-DIGEST.md` is a useful 2026-08-30 snapshot but predates rows
73–93 and the period-two continuation.  Do not use it as the current index.

## Minimal routing by problem

### P1

Read:

1. `RESULTS-eventual-period.md` for the same-orbit reduction and constant cases.
2. `PATH.md` R1 plus sections 9.3–9.5 for the zero-set obligation.
3. `RESULTS-alt-trace-fiber.md` for the alternating-fiber normal form.
4. `experiments/rule30/p1-period2-invariant/README.md` for the current exact
   period-two map, certificates, and next theorem.

Do not rerun: larger finite-period SAT grids, fixed-depth ladders, generic
left-permutive arguments, bounded adjacent-column prediction, support-width
descent, periodic-mask contraction, or local additive rankings.

### P2

Read `PATH.md` R8 and section 9.3, then
`RESULTS-orbit-closure-diagnostic.md` and
`RESULTS-checkerboard-growth-extended.md`.  Uniform Bernoulli invariance and
almost-everywhere density `1/2` are known but miss the lone seed by obstruction
E.  Checkerboard-patch growth is quantitative finite evidence, not a proof of
orbit-closure membership.

### P3

Read `PATH.md` R9, obstructions D/G/I, and rows 91–93.  The deterministic fuel
instrument is validated but no evolutionary search ran.  Exact succinct-index
circuit synthesis gives bounded results only.  Do not infer a work lower bound
from arbitrary-input ANF degree, one derivation system, proof size, or a fitted
runtime exponent at small `n`.

## Current P1 period-two frontier

Target for every nonzero finite configuration `y`:

```text
Tr_0(y) != Tr_0(F^2(y)).
```

Constant traces are already excluded.  The remaining phase is `0101...`
(the opposite phase maps to it after one Rule 30 step).

The strongest exact coordinates now are

```text
C = I(A OR (1 OR (B << 1))),
D = I(C OR (A << 1)),
pin = D & 1,
(A,B) -> (D,C),
```

where `I` is inverse Gray code.  For a genuinely realizable right half,
`rho_k=s(2k,1)` has no adjacent ones.  Neither fact has yet yielded mortality.

Best next theorem:

> If a no-`11` word `rho` has eventually-zero full forced-left reconstruction
> `L(rho)`, then `rho` is eventually periodic.

That would make the adjacent width-two trace eventually periodic, contradicting
the recorded width-two theorem.  The proof must control the full cumulative
boundary offsets and irregular isolated pulses; fixed summaries and longer
lookahead are already certified failures.

## Do-not-repeat obstruction screen

Reject a proposal immediately unless it explains why these do not apply:

| ID | Obstruction |
|---|---|
| A | Trace/boundary propagation reaches `O(log t)` depth while the target is `Theta(t)` away |
| B | The argument also excludes Rule 90's known periodic center |
| C | A 2D/density statistic changes only `O(1/W)` when column zero is overwritten |
| D | The proposed shortcut names but does not derive its exact composition/seam law |
| E | An ensemble or almost-everywhere theorem does not cover the lone-seed orbit |
| F | A fixed-depth strip leaves a new free outer boundary |
| G | Arbitrary-input complexity says nothing about evaluating one fixed input |
| H | Finite data cannot prove an infinite statement |
| I | Satisfiable fixed-input proof systems hit a small `Theta(n^2)` derivation ceiling rather than a lower bound |

Full hypotheses and affected rows are in `PATH.md` section 7.3 and
`FINDINGS.md` section 5b.

## Publication routing

- The zero-tail theorem has manuscript, Lean/SMT artifacts, figures, and a
  hostile audit under `docs/rule30/paper/`.  Its novelty still depends on
  checking the original Jen premise noted in `paper/PUBLICATION-NOTES.md`.
- Period-two work currently supports a methods/negative-results appendix, not
  a P1 claim.  Cite its raw `RESULTS-*` files and solver-free verifiers.
- P2/P3 reports are bounded or conditional and must retain those qualifiers.
- External prize-resolution claims by Fradkin and Topal are refuted in the
  corresponding `REFUTATION-*` files; cite the full audits, not this summary.

## Resumption discipline

1. Inspect process and Git state.
2. Choose one live theorem, not a topic survey.
3. Read only the sources routed above plus the exact predecessor result.
4. State how the proposal uses Rule 30's OR, the single orbit, and finite
   support.
5. Preregister the certificate class, controls, bounds, and kill conditions.
6. Prefer a finite human-checkable certificate; treat enumerations only as
   falsifiers.
7. Update this index only after exact controls and an independent verifier pass.
