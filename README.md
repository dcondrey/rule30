# Rule 30 Prize Research

[![Research status](https://img.shields.io/badge/status-active%20research-blue)](https://github.com/dcondrey/rule30)
[![Prize problems solved](https://img.shields.io/badge/prize%20problems%20solved-0%20of%203-red)](https://rule30prize.org/)
[![Reproducibility](https://img.shields.io/badge/reproducibility-exact%20checks%20%2B%20audit%20logs-green)](docs/rule30/START-HERE.md)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0003--1849--2963-green.svg)](https://orcid.org/0009-0003-1849-2963)

**A proof-oriented, adversarially checked investigation of the three Wolfram
Rule 30 Prize Problems.**

Rule 30 is a one-dimensional cellular automaton whose local update is

```text
F(x)(i) = x(i-1) XOR (x(i) OR x(i+1)).
```

Starting from one black cell, this tiny rule produces a center column for
which three basic questions remain open. The
[Wolfram Foundation offers three $10,000 prizes](https://rule30prize.org/),
one for each question.

> **Research status:** all three prize problems remain open. This repository
> proves partial results, derives exact reductions, records bounded evidence,
> and preserves machine-checkable failures of tempting proof strategies. It
> does **not** claim a prize solution. A finite computation, fitted asymptotic,
> or plausible invariant is never reported here as a theorem about the
> infinite Rule 30 orbit.

## The three problems

| Problem | Official question | Status here | Strongest live edge |
|---|---|---|---|
| **P1** | Does the center column always remain non-periodic? | **Open** | Exclude a nonconstant period-two center trace for every nonzero finite row |
| **P2** | Does each color occur equally often on average in the center column? | **Open** | Bridge ensemble results to the single-seed orbit |
| **P3** | Does the `n`th center cell require at least `O(n)` computational effort? | **Open** | Prove a fixed-sequence work lower bound in an explicit computation model |

The exact problem statements and submission rules are maintained at
[rule30prize.org](https://rule30prize.org/).

## What has been established

### Eventually constant center traces are excluded

The project contains proof-level classifications of the constant-zero and
constant-one trace fibers for nonzero finite configurations. Combined with the
same-orbit reduction, these exclude eventually constant center traces. The
zero-tail argument has a manuscript, independent proof artifacts, figures,
and a hostile audit under [`docs/rule30/paper/`](docs/rule30/paper/).

This is a genuine rung toward P1, but it does not exclude nonconstant periods.

### The period-two problem has an exact finite-word form

The current P1 target is

```text
For every nonzero finite y, Tr_0(y) != Tr_0(F^2(y)).
```

After reducing the two alternating phases to one and applying inverse Gray
code, survival is governed by the exact macro

```text
C = I(A OR (1 OR (B << 1)))
D = I(C OR (A << 1))
survive iff D is odd
(A, B) -> (D, C).
```

The associated four-state carry actions generate the dihedral group `D8`.
This explains exactly why several natural contraction, bounded-summary, and
local-ranking arguments fail. Those failures are preserved as independently
checkable negative certificates rather than discarded experiments.

The current strongest finite-rank reduction is a deterministic growing queue.
For either constant cut tail `c in {2,3}`, reverse the full newest dependency
diagonal `R` and scan

```text
S_0=c,  S_i=g_(S_(i-1))(R_i).
```

The final scan state uniquely emits or rejects the next hard-core endpoint.
Mortality of every such finite queue would prove the period-two rung.  The
exact quotient `3 -> 1` reduces its nonleading alphabet to three symbols, and
every normalized successor avoids `20`, `22`, and `011`; the all-length
mortality induction remains open.  The exact survival-language morph expands
minimal DFA rank, so the remaining target is an amortized proof that its
shortest accepted queue tends to infinity.  This minimum now has an exact
graph form: at horizon `h`, it is one plus product-graph distance from the
constant height-`h+1` frontier to the `F_(h+3)` hard-core inverse-cone
diagonals, with the invariant suffix DFA as the second factor.  The bare
frontier graph handles arbitrary queues.  Proving either equivalent distance
divergence would close the period-two rung.

There is now a uniform ordered descent inside each successful queue update.
After removing the newly appended boundary symbol, the transformed old
coordinates are strictly smaller in colex order for both `0<2<1` and
`2<0<1`.  Hence the rightmost decisive input is always a `1`, replaced by
`0` or `2`.  Finite synchronous products prove this for words of every
length.  It is not yet mortality: an appended boundary `1` can replace the
consumed pivot at a newer coordinate, so the remaining task is an ancestry
bound on those replacements.

Conditioning the terminal set on the complete actual Rule 30 right cone
raises the tail-2 minimum from `18` to `23` at horizon 12 and changes exact
`D8` phase costs.  The conditioned sets form a uniform inverse subsystem, but
rank descent may prepend a finite artificial endpoint prefix.  Whole-prefix
conditioning is therefore too strong for the application; actual-right
information must be imposed beyond that prefix, as in the scale-block
reduction.

No period-two impossibility theorem has yet been proved.

### Bounded P2 and P3 evidence is reproducible

The repository also contains:

- exact center-column and subword-complexity measurements through recorded
  finite horizons;
- checkerboard-patch growth measurements with bit-exact kernel cross-checks;
- bounded circuit-synthesis and proof-complexity probes;
- a deterministic word-RAM fuel instrument for evaluating proposed P3
  algorithms; and
- literature audits that separate valid prior results from claims whose
  decisive step or numerical evidence fails verification.

None of these bounded results closes P2 or P3.

## Start here

The project is deliberately layered so that resuming one question does not
require loading the full research history.

1. Read [`START-HERE.md`](docs/rule30/START-HERE.md) for current status, live
   theorem targets, and the compact attempt router.
2. Use [`EXPERIMENT-ATLAS.md`](docs/rule30/EXPERIMENT-ATLAS.md) to compare
   experiment assumptions, state representations, evidence levels, failure
   modes, and compatible synthesis opportunities.
3. Consult [`FACT-INDEX.md`](docs/rule30/FACT-INDEX.md) for exact identities,
   proved facts, controls, and reusable obstructions.
4. Open [`PATH.md`](docs/rule30/PATH.md) only when auditing the complete attempt
   register or checking whether an idea has already been tried.

For the active period-two P1 effort, go directly to the
[`p1-period2-invariant` resumption sheet](experiments/rule30/p1-period2-invariant/README.md).
It explicitly maps geometric ideas—run-size digits, pyramid operators,
touching-color counts, left/right imbalance, row toggles, and oscillations—to
the precise tests and counterexamples already on record.

## Reproduce the core checks

Requirements: Python 3.11 or newer and
[`uv`](https://docs.astral.sh/uv/). The core P1 verifiers use bounded memory
and finish in seconds on a typical development machine.

```bash
git clone https://github.com/dcondrey/rule30.git
cd rule30

PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/derive_and_controls.py
PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/verify_negative_certificate.py
PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/verify_moment_negative.py
PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/verify_divergence_negative.py
PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/bilateral_hardcore.py
```

Expected headline checks:

| Check | Expected result |
|---|---|
| `F^2` truth table | 32/32 pass |
| Two-orbit defect recurrence | 64/64 pass |
| Rule 90 control `{-1,1}` | Zero center through the configured horizon |
| Rule 30 adversarial row `{-8,-1,6}` | Alternates through time 14 and fails at 15 |
| Radius-eight Rule 30 rows | 131,071 nonzero rows checked |
| Local-ranking certificates | Pass without a solver |
| Moment/Hasse checks | 589,824 exact checks |
| Gray macro checks | 34,952 exact legal frontiers |

The scripts state their finite bounds. Passing them validates the identities
and negative certificates they implement; it does not prove P1.

## Research map

| Path | Purpose |
|---|---|
| `docs/rule30/START-HERE.md` | Compact status and attempt router |
| `docs/rule30/EXPERIMENT-ATLAS.md` | Cross-examination matrix, correlations, and synthesis queue |
| `docs/rule30/FACT-INDEX.md` | Theorem, identity, control, and obstruction index |
| `docs/rule30/PATH.md` | Exhaustive internal and external attempt register |
| `experiments/README.md` | Executable-artifact directory router |
| `docs/rule30/paper/` | Zero-tail manuscript and publication audit |
| `experiments/rule30/p1-period2-invariant/` | Current P1 derivations and exact certificates |
| `experiments/rule30-subword-extended/` | P2 center-word and factor-complexity measurements |
| `experiments/openevolve-p1-cocycle/` | P1 adaptive-rank conjecture search and width-18 falsifier |
| `experiments/openevolve-p1-rank-zero/` | Exact zero-tail OpenEvolve/GA witness search |
| `experiments/openevolve-p3/` | P3 evaluator and deterministic fuel instrument |
| `experiments/overnight-arms/` | Preregistered exploratory arms and raw findings |
| `runs/` | Preserved run manifests and verifier outputs |

Large regenerable arrays, compiled binaries, vendored dependencies, and
restart caches are intentionally excluded from Git. Compact results,
checksums, source code, preregistrations, and human-readable reports remain
versioned.

## Branch policy

| Branch | Purpose |
|---|---|
| `main` | Canonical verified archive and shared indexes |
| `p1` | Problem 1 theorem and experiment work |
| `p2` | Problem 2 density and subword work |
| `papers` | Manuscripts, venue work, and publication revisions |

Branches isolate changes; they do not erase shared evidence. Merge a topic
branch into `main` only after its preregistered controls and result report
pass. Create a P3 branch only when there is a concrete new P3 target rather
than another broad search.

## Research-integrity policy

- Status words are used literally: `PROVED`, `KNOWN`, `VERIFIED`, `EXACT
  COMPUTATION`, `FALSIFIED`, `KILLED`, `STALLED`, or `OPEN`.
- Every numerical claim is treated as a recorded result until independently
  reproduced.
- Rule 90 with finite row `{-1,1}` is the standing negative control for
  generic P1 arguments.
- Preregistrations and exact negative certificates are retained to prevent
  outcome-dependent retelling and repeated failed searches.
- Publication claims cite the full proof or result document, never a compact
  index.
- Model agreement, simulation depth, and fitted curves are evidence-generation
  tools—not substitutes for proof.

Reproduction failures, exact counterexamples, and corrections are welcome as
GitHub issues. A proposed prize solution should be accompanied by a complete,
uniform proof and independently checkable artifacts.

## Current best next theorem

The cleanest finite-word target is now the **projected diagonal-support
lemma**.  If
`s_c(W)` is the legal continuation length inside the exact forced block
`R_c(W)`, it is enough to prove for every nonempty hard-core word `W` that

```text
s_2(W) <= |W|,
s_3(W) <= |W| + 1.
```

Zero the source coordinates successively from left to right.  At survival row
`j`, it is enough to prove one adjacent change at some token `k>=j`, using
only `(alpha,beta)` for tail 2 and `(alpha,gamma)` for tail 3 (the latter only
through the final nonfinal row).  No matching or greedy history is required.
The claim has zero failures on the complete hard-core corpus through length
23; its held-out unrestricted tail-2 supplement alone contains 111,899 cases.
This is a uniform conjecture, not a proof.  An independent one-credit halving
recurrence also passes through length 23 and would suffice if proved.  Its
held-out refinement uses the fixed child `(left half, tail 2)` for both parent
tails and passes 365,414 cases.  See
`RESULTS-PROJECTED-DIAGONAL-HALVING.md`.  Pointwise derivative, affine-rank,
reverse-order, local edge-monotonicity, and literal half-block embeddings have
exact counterexamples.

A new output-only bridge gives a potentially cleaner route. Peeling one core
symbol is the fixed local map

```text
(Peel x)_t = tau_(swap(x_(t-1)))^(-1)(x_t).
```

Thus a finite core produces an eventually `Peel`-nilpotent cut. Proving that
the inverse-terminal cut of a hard-core endpoint is never finitely
`Peel`-nilpotent would settle the period-two rung only—not all of Prize
Problem 1. See `RESULTS-DYADIC-EXCEPTION-SEPARATOR.md` in the period-two
directory.

The inverse-terminal and Peel triangles now satisfy the exact rotated law
`P(I(sigma e))=sigma^2 I(e)`.  Combined with preservation of a finite
rightmost nonzero cell, it excludes every eventually periodic hard-core
endpoint from finite Peel rank, including rank zero.  Every remaining
collision must have an aperiodic endpoint; positive tail ranks grow exactly
as `m,m+1,...`.  See `RESULTS-ROTATED-PEEL-IDENTITY.md` in the same directory.

## Authorship and citation

Research and manuscript author: **David Lee Condrey**, WritersLogic, Inc.
([ORCID 0009-0003-1849-2963](https://orcid.org/0009-0003-1849-2963)).

Until a citable release or paper DOI is assigned, cite the specific commit and
the exact `RESULTS-*` or manuscript file supporting the claim. No open-source
license has yet been selected for the repository; absent an explicit license,
the contents remain under their applicable default copyright terms.
