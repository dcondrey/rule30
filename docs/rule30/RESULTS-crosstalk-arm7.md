# Crosstalk ARM7 bounded run

## Outcome

The bounded application run produced no surviving candidate.  This rejects
six concrete proposals; it does **not** falsify every possible dyadic or
query-specific algebra.

Bundle: `runs/rule30-arm7`

- two generations, three candidates per generation;
- twelve reserved evolution model-call slots;
- six critic rejections below the retention threshold;
- zero objective verification records and zero surviving native candidates;
- bundle integrity `PASS`;
- scientific release `NOT ESTABLISHED`.

## Useful rejection memory

The proposals failed for repeatable structural reasons:

1. Boundary vectors still contained `Theta(n)` bits or required linear seam
   propagation despite being labelled polylogarithmic.
2. Carry/error summaries required generating every nonlinear error event at
   their leaves, so the claimed compression began only after full simulation.
3. Polynomial carry corrections were asserted without an exact derivation and
   overlapped the carry-polynomial family already falsified at `n=2`.
4. Hashed boundary fingerprints assumed, rather than proved, that the missing
   seam correction was determined by the hash.
5. Several parent operations named helpers such as `correction` or
   `reconstruct_left_boundary` without defining executable functions.

Those fingerprints belong in the exclusion ledger.  None is evidence that all
other state representations fail.

## Synthesis audit

The final model synthesis overreached in two ways:

- It described ARM6 as proof that the center sequence is not 2-automatic,
  although ARM6 explicitly says finite data cannot establish that claim.
- It generalized six failed proposals and finite vocabulary scaling into a
  conjecture that no exact polylogarithmic dyadic algebra exists, then called
  the line "sharply falsified."

Crosstalk's scientific-release gate correctly prevented release, but the
headless prose was still too authoritative.  The application now:

- tells deliberating models to preserve source-stated claim boundaries and not
  infer universal nonexistence from finite measurements or rejected samples;
- labels unreleased output as **Unverified model synthesis**;
- prints the release blockers and explicitly warns that rejected candidates
  and finite measurements do not establish universal claims;
- exposes the same status and warning in JSON and investigation reports.

The focused investigation and bundle tests pass after this change.

## Next arm

ARM8 follows the purpose of the challenge more closely: quotient the causal
computation by its effect on the requested center bit rather than preserving
whole-tile identity.  Standard ROBDD states also grow exponentially in the
tested range, but their strong right-to-left advantage identifies a more
specific asymmetry for the next representation to exploit.
