<!-- repo-header:start -->
<img src="https://github.com/dcondrey.png?size=160" alt="Rule 30 Prize Research logo" width="120" align="left">

<h1>Rule 30 Prize Research</h1>

<p><strong>Proof-oriented, reproducible research on the Wolfram Rule 30 Prize Problems: partial theorems, exact certificates, and audited experiments.</strong></p>

<br clear="left">

[![Best Practices Evidence](https://img.shields.io/badge/best%20practices-evidence%20reviewed-6a4c93?style=flat-square&labelColor=20232a)](.bestpractices.json) [![GitHub Sponsors](https://img.shields.io/badge/GitHub%20Sponsors-Sponsor-EA4AAA?style=flat-square&labelColor=20232a)](https://github.com/sponsors/dcondrey) [![Research status](https://img.shields.io/badge/status-active%20research-blue?style=flat-square&labelColor=20232a&color=brightgreen)](https://github.com/dcondrey/rule30) [![Prize problems solved](https://img.shields.io/badge/prize%20problems%20solved-0%20of%203-red?style=flat-square&labelColor=20232a)](https://rule30prize.org/) [![Reproducibility](https://img.shields.io/badge/reproducibility-exact%20checks%20%2B%20audit%20logs-green?style=flat-square&labelColor=20232a)](docs/rule30/START-HERE.md) [![ORCID](https://img.shields.io/badge/ORCID-0009--0003--1849--2963-green.svg?style=flat-square&labelColor=20232a&color=A6CE39)](https://orcid.org/0009-0003-1849-2963)
<!-- repo-header:end -->

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
2. Consult [`FACT-INDEX.md`](docs/rule30/FACT-INDEX.md) for exact identities,
   proved facts, controls, and reusable obstructions.
3. Open [`PATH.md`](docs/rule30/PATH.md) only when auditing the complete attempt
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
| `docs/rule30/FACT-INDEX.md` | Theorem, identity, control, and obstruction index |
| `docs/rule30/PATH.md` | Exhaustive internal and external attempt register |
| `docs/rule30/paper/` | Zero-tail manuscript and publication audit |
| `experiments/rule30/p1-period2-invariant/` | Current P1 derivations and exact certificates |
| `experiments/rule30-subword-extended/` | P2 center-word and factor-complexity measurements |
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

The most focused live target is the following period-two bridge:

> **Hard-core isolated-pulse theorem.** If a binary sequence `rho` has no
> adjacent ones and its complete forced-left Rule 30 reconstruction is
> eventually zero, then `rho` is eventually periodic.

It retains the three hypotheses lost by earlier finite-state ladders: Rule
30's nonlinear OR, the relationship between both sides of the same orbit, and
finite spatial support. A proof would settle the period-two rung only—not all
of Prize Problem 1.

## Authorship and citation

Research and manuscript author: **David Lee Condrey**, WritersLogic, Inc.
([ORCID 0009-0003-1849-2963](https://orcid.org/0009-0003-1849-2963)).

Until a citable release or paper DOI is assigned, cite the specific commit and
the exact `RESULTS-*` or manuscript file supporting the claim. No open-source
license has yet been selected for the repository; absent an explicit license,
the contents remain under their applicable default copyright terms.
