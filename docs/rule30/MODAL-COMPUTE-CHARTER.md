# Rule 30 Modal compute charter

## Authority and hard boundary

The user authorized at most **$200 USD of lifetime Modal expenditure** for the
Rule 30 investigation.  This is a ceiling, not a target.  It authorizes Modal
infrastructure only; it does not authorize model-provider calls or another
cloud service.  Billing-cycle resets do not reset this research budget.

No paid job may be submitted merely because budget remains.  The local guard
in `experiments/rule30/modal_guard.py` must first admit and reserve it.

## Admission invariants

Every experiment is preregistered as JSON under schema
`crosstalk.rule30.modal-experiment.v1`.  Admission fails unless the manifest
contains all of the following:

- one stable analysis-family identifier;
- an exact hypothesis and unresolved question;
- at least two predicted outcomes that cause different next decisions;
- an explicit kill condition;
- a prior-art search no more than 30 days old, two distinct immutable source
  snapshots, the closest known result, and the proposed novel delta;
- the local negative-result documents that were checked;
- exact code, runtime, algorithm, solver, seed, and work-unit identities;
- a current `modal billing rates --json` snapshot;
- CPU, memory, timeout, and a safety multiplier of at least 1.25;
- no worker network access, no GPU, no retries, and no resubmission after an
  ambiguous failure.

The guard hashes the actual method and each work-unit payload.  Pricing changes,
titles, and cosmetic renaming do not change those identities.  The lifetime
SQLite ledger places a unique constraint on every work-unit hash.  Once a unit
has been reserved, submitted, completed, failed, or become ambiguous, it cannot
be admitted again.

This prevents exact computational duplication.  Semantic overlap with obscure
prior work cannot be decided by a hash, so the documented literature review is
a separate mandatory human/research gate.  Discovery of prior art cancels the
compute job and is itself a useful zero-cost outcome.

## Staged release

The guard enforces cumulative reservations, using the full timeout cost rather
than an optimistic runtime estimate:

| Stage | Cumulative ceiling | Opens only after |
|---|---:|---|
| calibration | $5 | synthetic infrastructure manifest |
| pilot | $20 | passed calibration |
| expansion | $50 | informative pilot |
| targeted | $100 | informative expansion |
| verification | $200 | targeted survivor; independent implementation |

Every later manifest names its prerequisite job IDs.  A prerequisite must have
completed, have a result digest, and have passed its preregistered information
gate.  Unused money remains locked.  A terminal failure never opens the next
stage.

## Platform execution rule

Modal Functions can be restarted after a container failure or preemption even
when application retries are disabled.  Therefore the strict path uses short,
CPU-only, network-disabled Modal Sandboxes, which Modal documents as
nonpreemptible when no GPU is attached.  A remote runner must still treat every
operation as idempotent, terminate each sandbox immediately, and never resubmit
an unknown outcome.  The maximum cost of an ambiguous unit must remain small.

The local scheduler guarantees at-most-one intentional submission.  It must not
claim that an external platform provides a mathematical exactly-once execution
guarantee.

## Explicit exclusions

The authorized budget will not be used for:

- regenerating published center-column prefixes;
- larger reruns of compression, recompression, reflection, rotation, zero-
  pattern, image, quadtree, ROBDD, parity-survival, or transfer-monoid probes;
- another measurement whose only output is that Rule 30 looks complex or
  random;
- generic model brainstorming or GPU inference;
- a test whose possible outcomes do not alter the next research decision;
- a candidate that lacks an exact mechanism and executable bounded contract.

## First eligible scientific target

After a synthetic calibration, the first eligible pilot is a bounded
periodicity-assumption contradiction search.  It must encode an assumed center
period, use Rule 30's exact nonlinear recurrence and lone-seed boundary, include
Rule 90 as an adversarial control, and return a reusable certificate such as a
minimal contradiction, transition graph, or candidate period-independent
invariant.  Merely extending the checked period range is not a successful
outcome and cannot open the expansion stage.

## Local workflow

Validation and reservation are intentionally separate from remote execution:

```bash
python experiments/rule30/modal_guard.py validate MANIFEST.json --repo-root .
python experiments/rule30/modal_guard.py reserve MANIFEST.json \
  --repo-root . --ledger PRIVATE_LEDGER.sqlite3
python experiments/rule30/modal_guard.py status --ledger PRIVATE_LEDGER.sqlite3
```

The ledger is operational state and should not be committed if it contains
remote invocation identifiers.  Manifests, rate snapshots, result hashes, and
scientific certificates should be archived with the investigation.
