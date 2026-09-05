# Result: amortized drift/credit potential killed by its own 4th kill bullet

Date: 2026-09-04. Executes `PREREGISTRATION-ENDPOINT-ENERGY-INVARIANT.md`
sections 4 (Setup 1-4) and 6 (controls). Written up directly from
`verify_endpoint_energy_invariant.py`'s full log
(`verify_endpoint_energy_invariant_20260904.log`) after the executing agent
completed the run but stopped before writing this file itself.

**Verdict up front: killed, by the preregistration's own "reduces to the
killed object" bullet, corroborated by "no absorption structure."** For
every one of the top 5 partitions carried forward to the full `n=9..18`
stability sweep, the single most-recent D8 class `sigma_{j-1}(w)` alone
predicts death **at least as well as, and consistently better than**, the
full unbounded running-history charge `k(w,j)`. The whole point of this
document's proposed mechanism (section 3b) was that history should add
something beyond the current-state snapshot that BACKLOG item 4 already
showed was vacuous; it does not.

**Important caveat on scope, found after this design was registered:**
`RESULTS-MEASURE-SUPPRESSION.md`'s V3(b) check (same day) established that
`flip_pairing.forced_orbit`'s survivor population -- the object `N_j`,
`S_j`, and the D8 class sequence `sigma_j(w)` used throughout this
document -- is the `(BWH+)`/`Psi_n` construction, not `H_r(n)`/DLP-RW
(`BACKLOG.md` section 17's correction note). This document's target
(section 1: "same numerical target already on record... the counting
line... exactly as defined in `flip_pairing.py`") inherited that mislabel.
So even had the drift mechanism survived, it would have been a fact about
`(BWH+)`/`Psi_n`, not about the DLP/RW route this project is actually
pursuing. That does not change today's verdict (the mechanism fails on its
own terms regardless), but it means this route would need to be
re-registered against `literal_extension`'s actual `H_r(n)` construction
before it could bear on RW at all, not merely re-run.

## 1. What was run

`verify_endpoint_energy_invariant.py` (throwaway, not wired into any
pipeline), against `flip_pairing.forced_orbit`/`census` unmodified, plus a
new D8-class extraction added only in this script (not modifying
`flip_pairing.py`). Exhaustive over all `2^n` sources, `n=9..18`, both
`c in {2,3}`.

**Control 1 (regression check).** The extended census reproduces
`block_halving.py`'s own `k` values from the same computation:
`n=9,c=2: k=1`; `n=9,c=3: k=4`; `n=12,c=2: k=2`; `n=12,c=3: k=2`;
`n=16,c=2: k=1`; `n=16,c=3: k=2` -- all `<= 4`, consistent with the
already-recorded `k<=3` for the measured `n=11..18` range (the one `k=4` at
`n=9,c=3` is below that range and does not contradict it). Confirms the
instrumentation did not silently change the underlying forced-orbit
computation.

**Partition screen.** All 128 partitions of the 8 D8 classes into
`F`/`F^c` swept exhaustively at `n=9..12`, both `c` (8 (n,c) cells per
partition). Top 5 by `|mean r|` carried forward to the full `n=9..18`
sweep, per the preregistration's stated tractability compromise:
`F=[0,1,4,5]`, `F=[0,2,3,6,7]`, `F=[0,2,3,7]`, `F=[0,1,4,5,6]`,
`F=[0,1,5]` (class indices as produced by the D8 extraction used
elsewhere in this project).

## 2. Stability across n=9..18

All 5 partitions show a correlation `r(k(w,j), death@j)` that is
**real, sign-stable, and non-vanishing** from `n=9` through `n=18`
(e.g. `F=[0,1,4,5]`: `-0.137` at `n=9` to `-0.100/-0.110` at `n=18`,
no sign flip, no decay to zero across 5 doublings of the source space).
This part of the design succeeded: the correlation is not a small-`n`
finite-size artifact (rules out the preregistration's "unstable sign" kill
bullet).

## 3. Shuffle control (Control 3): passes, correlation is real, not a marginal-distribution artifact

For every partition and every `(n,c)` checked (`n=12,16`), the real
correlation (`~-0.10` to `~+0.12`) collapses to noise (`|r| < 0.02`, mostly
`< 0.01`) under the shuffle (permuting each survivor's own class sequence
before recomputing `k`). Example: `F=[0,2,3,6,7], n=16, c=2`:
`r_real=+0.1070`, `r_shuffled=-0.0097`. This rules out the "reduces to a
marginal-distribution artifact" failure mode named in Control 3 -- the
effect genuinely depends on temporal order, not just on the per-level class
distribution.

## 4. Kill check ("reduces to the killed object"): FIRES

This is the decisive negative result. For every partition, at `n=16`, both
`c`:

```
F=[0, 1, 4, 5]:       r(k,death) = -0.1095 / -0.1106   r(sigma_(j-1) in F, death) = -0.1465 / -0.1721
F=[0, 2, 3, 6, 7]:    r(k,death) = +0.1070 / +0.1018   r(sigma_(j-1) in F, death) = +0.1565 / +0.1740
F=[0, 2, 3, 7]:       r(k,death) = +0.1188 / +0.1057   r(sigma_(j-1) in F, death) = +0.1669 / +0.1746
F=[0, 1, 4, 5, 6]:    r(k,death) = -0.1095 / -0.1059   r(sigma_(j-1) in F, death) = -0.1574 / -0.1731
F=[0, 1, 5]:          r(k,death) = -0.1013 / -0.1012   r(sigma_(j-1) in F, death) = -0.1593 / -0.1740
```

In **every single row**, conditioning on `sigma_{j-1}(w)` alone (the
current-state snapshot BACKLOG item 4 already tested and killed) predicts
death *more strongly* than the full unbounded running-history charge
`k(w,j)`. The running sum adds no information beyond the most recent step
-- the opposite of what section 3b's mechanism needed ("does the running
sum... correlate with imminent death, which complete branching does not
address at all"). This is precisely the preregistration's 4th kill bullet:
*"the only partitions `F` that show any correlation are ones where the
correlation is fully explained by `sigma_{j-1}(w)` alone... has silently
rediscovered BACKLOG item 4's already-killed per-step class potential
wearing a running-sum disguise."*

## 5. Corroborating signal: no absorption structure

`Var(k | alive @ j)` for the 4 partitions with nonzero correlation grows
with `j` rather than saturating (e.g. `F=[0,2,3,7]`: `j4:1.12 -> j6:2.15`,
`F=[0,1,5]`: `j4:0.80 -> j6:0.90 -> j8:1.91`) -- the signature the
preregistration's 3rd kill bullet asks for ("its variance keeps growing
linearly in `j` among survivors, rather than saturating near the death
threshold"). This is independent corroboration that even where a real,
shuffle-robust correlation exists, it is not behaving like an absorbed
random walk approaching a death threshold, which is what the gambler's-ruin
argument in section 3b of the preregistration required. (One partition,
`F=[0,1,4,5]`, logged `Var=0.00` at every `j` shown at `n=16,c=2` --
inconsistent with that partition's own nonzero shuffle-control correlation
elsewhere in the same run; this is flagged as a probable bug or edge case
in the variance computation for that specific partition/level combination,
not trusted as a genuine zero, and does not change the verdict since the
other three partitions independently show the same non-saturating pattern.)

## 6. Bottom line

Two independent kill signals (4th bullet directly, 3rd bullet
corroborating) both fire. The amortized/drift mechanism proposed in this
preregistration is dead, on the same underlying fact BACKLOG item 4 already
established (complete branching / no information beyond the current
state) -- section 3b's premise that "a deterministic, high-state process
can still produce output whose *running history* predicts death better
than its current state" is not supported by the data. This does not kill
the counting-line inequality itself (still open, unproven, and now known
to require re-deriving for the correct `H_r(n)` object rather than
`(BWH+)`/`Psi_n`), only this specific proof mechanism.

## 7. What this does not claim

- Does not claim the counting line, RW, DLP, or PT2 is true or false.
- Does not claim no history-dependent mechanism could ever work -- only
  that a running D8-class charge, under the partitions screened here, does
  not outperform the current state, which is what this document's own
  kill condition was built to detect.
- Does not claim this result bears on `H_r(n)`/DLP-RW directly; per section
  0 above, the object tested here is `(BWH+)`/`Psi_n`, mislabeled as RW at
  the time this preregistration was written.
- Every number above is from `verify_endpoint_energy_invariant_20260904.log`,
  produced by the unmodified `flip_pairing.forced_orbit`, not reimplemented
  or estimated.
