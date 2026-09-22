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
- no worker network access, no retries, and no resubmission after an ambiguous
  failure;
- either no GPU, or a GPU admitted under the measured-justification gate below.

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

## GPU measured justification

GPU work was prohibited outright, and `modal_guard.py` phrased the prohibition
as lasting "until a separate measured justification exists".  That justification
now exists, so the clause becomes a gate rather than a ban.  The prohibition was
never about GPUs being expensive; it was about admitting a device whose output
nobody had checked.  What follows is the check.

**The measurement.**  `a20_deep_simulation` implements a warp-shuffle Rule 30
kernel (`rule30_kernel_v6.cu`, per-lane register chunks, tiled halos) and
measures **1.06e14 cell-updates/s** on an H100 at `R=16 H=16 W=4` with recording
compiled in.

**The validation, which is the part that matters.**  Throughput alone would
justify nothing; a fast wrong generator is worse than none.  The kernel's output
is checked three independent ways:

- **against an independent implementation** — full-output equality with a
  `gmpy2` generator sharing no code with the kernel, over 8 band runs and 72
  columns;
- **against the published record** — the centre column is bit-exact against the
  Wolfram Data Repository over **1,980,000 bits**, and against OEIS `b051023.txt`
  over **100,001 bits**;
- **against itself** — cross-run bit-identical, and the ablation's output proven
  bit-identical to the pre-optimisation revision on a shared layout.

This history is load-bearing in a way a passing test is not: the kernel was
**wrong** at first.  A recording-ownership defect let two tiles claim the same
column, and the first divergence was at bit 4,631 — past any short prefix gate,
and invisible to a 64- or 256-bit check.  `KERNEL-V6-DEFECT.md` records it.  The
justification is therefore evidence that this validation regime catches real
defects, not that the code looked correct.

**The gate.**  `modal_guard.py` admits `execution.gpu` as a device name, not a
flag, and only when the manifest carries `execution.gpu_measured_justification`
with the device, a measured throughput, what the output was validated against,
and `evidence` paths that resolve inside the repository.  The device must also
be priced in the rate snapshot as `gpu_second_usd`, and that rate is charged for
the full timeout on every work unit, so the stage ceiling covers the whole run
rather than its CPU fraction.  Every other invariant is unchanged: the ledger
stays mandatory, unit hashes stay unique for life, retries stay at zero, workers
stay off the network, and the staged ceilings still gate release.

**What this does not authorize.**  Three limits, none waived by this section:

1. The **explicit exclusion** on regenerating published center-column prefixes
   still stands.  The validation above regenerates them as a correctness oracle,
   which is why it is evidence here rather than a scientific output; a run whose
   *product* is a longer published prefix is still excluded.
2. `execution.timeout_seconds` remains capped at **3600**.  A run longer than an
   hour must be split into resumable work units, each separately hashed and
   reserved.  A 3e9-step run is therefore at least six units, not one.
3. `execution.backend` must still be `modal-sandbox`.  The `a20` scripts use
   `@app.function`, which the platform execution rule above excludes as
   restartable.  Porting them is a prerequisite, not a formality.

**Retroactive entry.**  The `a20` arm ran before any of this existed: the guard
was imported by none of its scripts and no ledger was created, so no stage was
opened and no unit hash reserved.  It is booked against the calibration stage by
`modal_guard.py backfill`, which stores the row with status `completed` and
`"admitted": false` in its manifest JSON — the accounting statuses are fixed
(`reserved`, `submitted`, `ambiguous`, `completed`, `failed`) because
`_committed_total` refuses an unknown one, so the in-arrears fact lives in the
manifest rather than in a status of its own.

**The booked figure is a floor, not the total.**  $1.89 is what the 19 container
invocations still visible to `modal app list` come to (1,723 s of wall time at
the $3.95/hr H100 rate).  The calibrate, calibrate-v2, sweep-v3/v4/v5, deep-run,
race-a/b and agreement-runs invocations have aged out of that listing window and
are **not** included, so true spend is higher by an unmeasured amount.  The
authoritative number is on the Modal dashboard and has not been checked.  This
matters more than the size of the gap: the ledger is what every later
reservation reasons from, and an understated total is the one error that
compounds.  Anyone opening a paid stage should reconcile against the dashboard
first and re-book the difference.  The exposure remains procedural rather than
financial — the floor is $1.89 against a $200 lifetime ceiling — but "procedural"
is a judgement about the gap's size, and the gap is not measured.

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
