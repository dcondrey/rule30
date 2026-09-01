# Rule 30 research workspace

All three Wolfram Rule 30 prize problems remain open.  This repository contains
proved partial results, exact reductions, bounded experiments, failed-method
certificates, publication material, and reproducible code.  A finite check or
a useful reformulation is never to be reported as a prize result.

## Start here

Read these in order, stopping as soon as the current task is routed:

1. [`docs/rule30/START-HERE.md`](docs/rule30/START-HERE.md) — current status,
   attempt routing, live targets, and the minimal resumption protocol.
2. [`docs/rule30/FACT-INDEX.md`](docs/rule30/FACT-INDEX.md) — exact identities,
   proved facts, controls, and recurring obstructions.
3. [`docs/rule30/PATH.md`](docs/rule30/PATH.md) — exhaustive historical
   register.  Do not read it front to back unless auditing the whole project.

For the current period-two Problem 1 effort, go directly to
[`experiments/rule30/p1-period2-invariant/README.md`](experiments/rule30/p1-period2-invariant/README.md).

## Branch and worktree policy

`main` is the canonical archive: shared facts, exact certificates, and the
compact indexes remain available there.  Topic branches isolate new edits:

| Branch | Intended work |
|---|---|
| `rule30/p1` | Problem 1 theorem and experiment work |
| `rule30/p2` | Problem 2 subword-complexity work |
| `rule30/papers` | Manuscripts, venue work, and publication revisions |

Do not delete shared material merely to make a topic branch look smaller.
Use a sparse worktree when a focused filesystem view is needed; the branch
isolates history while sparse checkout limits visible paths and review cost.
Create such worktrees only from a clean checkout, and merge a topic branch
back to `main` only after its controls and result report pass.  Problem 3 is
currently archival; create `rule30/p3` from `main` only when a concrete new P3
target is approved.

## Directory map

| Path | Role |
|---|---|
| `docs/rule30/START-HERE.md` | Canonical compact attempt index |
| `docs/rule30/FACT-INDEX.md` | Canonical compact theorem/obstruction index |
| `docs/rule30/PATH.md` | Full internal and external attempt register |
| `docs/rule30/overnight/CONTEXT-DIGEST.md` | Historical digest frozen at 2026-08-30; useful but not current |
| `experiments/overnight-arms/frontier_attack/FINDINGS.md` | Canonical rows 73–90 and frontier-arm details |
| `experiments/rule30/p1-period2-invariant/` | Current focused period-two attempt and exact certificates |
| `docs/rule30/paper/` | Zero-tail manuscript and publication notes |
| `experiments/` | Reproduction code and compact results; large caches/build products are ignored |

## Research-integrity rules

- Status vocabulary is strict: `PROVED`, `KNOWN`, `VERIFIED`, `EXACT
  COMPUTATION`, `FALSIFIED`, `KILLED`, `STALLED`, or `OPEN`.
- Treat every numerical claim as recorded until independently reproduced.
- Rule 90 with finite row `{-1,1}` is the standing negative control for P1.
- Preserve preregistrations and exact negative certificates.  They prevent
  outcome-dependent retelling and repeated failed searches.
- Cite the original result document in publication work, not a compact index.
- Do not extend a bounded horizon merely because the last run was negative;
  first identify a uniform mechanism that escapes obstruction H.

## Resume checklist

```bash
ps aux | grep claude
cd /Volumes/A/researchpapers && git status --short --branch
```

Then read `START-HERE.md`, choose exactly one live theorem target, inspect only
its linked sources, preregister a falsifiable certificate class, and run the
standing controls before interpreting a candidate.
