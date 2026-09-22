# P1: max_zero_run is rotation-phase-dependent; a clean sub-case, and where it breaks

Date: 2026-09-11. Evidence in `experiments/rule30/r1-general-period/`:
`raw_necklace_sweep_p3_10.py`, `clustered_ones_rotation_sawtooth.py`,
`separated_gap_resonance_sweep.py`, and their JSON outputs. Follow-on to
[the modal-pilot width-saturation evaluation](RESULTS-p1-modal-pilot-width-saturation.md),
picking up its open direction: whether `max_zero_run` (the general-*p*
strip-contradiction certificate from `r1-general-period/survey.py`) has a
closed form for the general necklace population, not just the
`0^(p-1)1` isolated-one family the stored `survey-results.json` covers.

## 1. max_zero_run is not a function of the necklace class alone

`survey-results.json` stores one value per period for the isolated-one
family and reports it as *the* value for that period. That is only valid
because the stored rotation happens to be that family's maximum: sweeping
every rotation of the same cyclic word (`raw_necklace_sweep_p3_10.py`,
width 20, p=3..10, all 4570 non-constant necklace words) shows
`max_zero_run` genuinely depends on phase, not just on which cyclic word
is assumed periodic. This matters for reading any prior table in this
family of experiments: two rotations of the same period word are the same
periodicity hypothesis but can report very different certificates.

## 2. A clean, exact sawtooth for k=1 and k=2 adjacent ones

For a period-*p* word with a single contiguous block of *k* ones (rest
zeros), sweeping all *p* rotations at width 20 (`p=5..10`, six periods,
`clustered_ones_rotation_sawtooth.py`):

- **k=1** (`0^(p-1)1`, the isolated-one family): the rotation values form
  an exact arithmetic sequence, `p+2, p+1, p, ..., 4, [wrap to p+2]` —
  peak `p+2`, floor `4`, at every period 5 through 10.
- **k=2 adjacent** (`0^(p-2)11`): the same shape, one step down — peak
  `p+1`, floor `4`, at every period 5 through 10.

Both hold exactly, with **zero exceptions**, across all six periods
tested. The floor of 4 is period-independent for both families — a fact
not implied by anything in the earlier reports.

## 3. k=3 already breaks it

The same sweep for k=3 (three adjacent ones) does **not** follow
`peak = p-k+3`: p=5 through 10 give peaks 6, 13, 8, 8, 10, 11 against a
naive-extrapolated prediction of 5, 6, 7, 8, 9, 10 — matches only by
apparent coincidence at p=8, and p=6's value (13) is not a small
perturbation, it is close to double the prediction. The floor also stops
being the constant 4 (it becomes 5, or 11 at p=6). k=4 is worse still:
p=8 has no `DIES` rotation at all (every rotation `SURVIVES`), and p=9,
p=10 give peaks (13, 16) that exceed even the k=1 peak for the same
period. Adjacency of ones is not the right generalizing axis past k=2.

## 4. Separated ones are a different, resonant regime, already visible in the raw data

Two ones separated by unequal gaps (not adjacent) were not swept
exhaustively over rotations here, but the raw sweep already contains
clear examples: period-7 word `0001001` (gaps 2 and 3) reaches
`max_zero_run=21`, i.e. **3p**, far outside the `p+O(1)` band that both
clean sub-cases (k=1, k=2-adjacent) and the broken k=3/k=4 cases stay
within. Whatever governs that value is not captured by run-length or
adjacency statistics of the word — cyclic run lengths, one-count, and
block adjacency were checked directly against `max_zero_run` for every
`DIES` word in the p=5..10 population and none correlate simply. The gap
*pair* (2,3) recurring at the top of the p=7 table, and 2-adjacent-block
patterns like `01110100` recurring near the top of p=8's, suggests a
number-theoretic resonance between the gap structure and Rule 30's own
local dynamics, not a run-length effect — consistent with this repo's
existing Fibonacci/golden-ratio structure work elsewhere in
`p1-period2-invariant/` (`RESULTS-FIB-FIBER-UNIFICATION.md`,
`RESULTS-FIB-ABSENT-M8-M9-M10.md`), which was not cross-checked against
this data this session.

## 5. The resonance is sporadic, not a smooth trend — two easy hypotheses ruled out

Fixing `g1` and sweeping `g2` (equivalently `p`) rules out the two
cheapest explanations. Holding `g1=0` (adjacent, §2's clean case) gives
the tame, monotone `peak/p -> 1`. But `g1=1`: p=5 and p=8 have **no**
`DIES` rotation at all (every rotation survives), while p=6, 7, 9, 10 die
with peaks 9, 12, 17, 21 — not a monotone sequence in `p`, since the
family drops out entirely twice. `gcd(g1+1, g2+1)` does not separate the
survive/die cases (p=6 and p=8 both give `gcd=2`, one dies, one doesn't;
`separated_gap_resonance_sweep.py` computes the gcd for every gap pair
tested and confirms no clean split by it).
Holding `g1=2`: p=7 (gaps 2,3) spikes to `peak=21=3p`, but p=8, 9, 10
(gaps 4, 5, 6) immediately fall back to the same tame `~(p+1)/p` band as
`g1=0`. The (2,3) spike at p=7 is a singular outlier among its own
neighbors, not the start of a growing trend. Whatever produces it is
particular to that `(p, gap)` pair, not a function of `g1` alone or of
any gcd relation checked here.

## Conclusion

There is a genuine closed form, but only for the two sparsest clustered
cases (k=1, k=2-adjacent): peak `p+2-  (k-1)`, floor `4`, exact sawtooth
in rotation phase, no exceptions in six periods. It stops holding at
k=3. The population that actually decides whether a *general*
period-independent invariant exists is the separated-gap case, which
shows super-linear, apparently resonant behavior (3p at one already-found
example) that this session's structural statistics (run lengths, one
density, block adjacency) do not explain. That is real mathematics, not
a wider computation — matching what both this route's own
`PROOF-STATE-CAPSULE.md` and the modal-pilot report already said the next
step has to be.

## Verification

`raw_necklace_sweep_p3_10.py` recomputed nothing that wasn't already
validated: width 20 for p<=10 was shown sufficient in
`width_saturation_and_necklace_sweep.py` (§3 of the linked report), this
script only persisted the raw per-word mapping that computation had
discarded. `clustered_ones_rotation_sawtooth.py` reads that JSON and
recomputes rotations and peaks directly from it — no new CA runs. Both
scripts' JSON outputs are in the same directory for independent
re-derivation.
