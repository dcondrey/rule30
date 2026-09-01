# Rule 30 experiment directory

This directory contains executable probes, exact certificates, search logs,
and bounded data.  The experiments are intentionally not arranged as a
chronological proof: several directories contain controls or killed routes
whose value is to prevent a failed mechanism from being proposed again.

Start with
[`EXPERIMENT-ATLAS.md`](../docs/rule30/EXPERIMENT-ATLAS.md).  It provides:

- the authoritative register for every historical attempt;
- a dependency graph for the active period-two reduction;
- a cross-examination matrix stating what each experiment retains and loses;
- correlations between experiments that use the same exact local algebra;
- the current synthesis opportunities and their immediate falsifiers; and
- a standard record format for future experiments.

Do not infer a theorem from a directory name, a long run, or a passing finite
bound.  The status-bearing sources are the linked `RESULTS-*` files.

## Directory router

| Directory | Scope | Status-bearing source |
|---|---|---|
| `rule30/p1-period2-invariant/` | Active exact attack on the nonconstant period-two center trace | `rule30/p1-period2-invariant/README.md` and its `RESULTS-*` files |
| `openevolve-p1-cocycle/` | Search for a secondary rank on exact symbolic plateau edges | `../docs/rule30/RESULTS-openevolve-p1-cocycle.md` |
| `openevolve-p1-rank-zero/` | Adversarial finite witnesses for the rank-zero and constant-tail separators | `../docs/rule30/RESULTS-openevolve-p1-rank-zero.md` |
| `rule30/p1-period2-oboc/` | Older one-bit-output-certificate attempt | `rule30/p1-period2-oboc/RESULTS.md` |
| `rule30/p1_attack/`, `rule30/p1_constrained_attack/` | Earlier bounded P1 searches | `../docs/rule30/PATH.md` |
| `rule30/ladder/` | Fixed-period omega-automaton ladder | `../docs/rule30/RESULTS-ladder-rung0.md` and `RESULTS-ladder-rung1.md` |
| `rule30/orbit-closure/` | P2 lone-seed orbit-closure diagnostic | `../docs/rule30/RESULTS-orbit-closure-diagnostic.md` |
| `rule30-subword-extended/` | Long center-prefix and factor-complexity measurements | `../docs/rule30/RESULTS-subword-complexity-extended.md` |
| `openevolve-p3/` | P3 evaluator and deterministic word-RAM fuel instrument | `../docs/rule30/RESULTS-openevolve-p3.md` and `RESULTS-openevolve-p3-fuel.md` |
| `sygus-p3/` | Bounded exact circuit synthesis | `../docs/rule30/RESULTS-bounded-circuit-synthesis.md` |
| `overnight-arms/` | Preregistered exploratory arms, literature checks, and raw findings | `../docs/rule30/PATH.md` and `overnight-arms/frontier_attack/FINDINGS.md` |
| `rule30/proof-complexity/` | Bounded CNF/MUS/derivation probes | `../docs/rule30/RESULTS-proof-complexity-probe.md` |
| `rule30/p_geometric_attack/`, `p_fringe_attack/`, `p3_circuit_attack/` | Screened unconventional proposals | Their local assessment files and `../docs/rule30/PATH.md` |

Caches, virtual environments, compiled objects, and regenerated bulk arrays
are not research records.  Compact JSON outputs, exact witnesses,
preregistrations, solver certificates, independent verifiers, and logs needed
to audit an adaptive search are records.
