# Generalizing R1's zero-set machinery from period 2 to period p: the pin and the strip transfer cleanly, the five-zero theorem does not

Date: 2026-09-09.

**Deliverable: an idea tested, not closed. R1 and P1 remain open.** The pin
generalizes trivially (it already was general in `PATH.md`). The
family-seam strip method's soundness argument also generalizes cleanly, and
is demonstrated here with new code, not merely argued. The five-zero
theorem does **not** generalize as a uniform bound: the specific
generalized quantity measured here (the longest run of consecutive
centre-zero-time samples of column 1 that can be forced to zero) never gets
tighter than period 2's bound of 4, and for most tested periods and words
it gets strictly looser, in one family unboundedly so. This gives a
precise, quantified answer to why this route has stalled at `p=2`, and it
is a genuine structural finding, not a failure to search hard enough.

| Finding | Evidence |
|---|---|
| The pin (`c_t=1 => l_t` determined) is already period-general in `PATH.md` section 2; column `-1` eventually periodic `<=>` `r` eventually periodic on `{c_t=0}`, for ANY eventually periodic `c` | `R`, already on record, reproduced here |
| The realizable-sample language is regular for every periodic word, but **finite-type (a finite forbidden-factor set) only at `p=2`**; already recorded, reproduced independently here for `p=3` word `001` through forbidden length 12 | `R/C`, cites `RESULTS-alt-trace-fiber.md`, reproduced with `alt-trace-frontier/sample_filter.py` |
| The strip method's soundness argument transfers to any period `p` with no new argument needed, because it never used `p=2`; demonstrated, not just argued, by new code that reproduces the frozen `p=2` strip's stable sets **exactly** | `C`, bit-for-bit regression, two widths |
| Generalized five-zero quantity at `p=2`: max forced run of zero rho-samples is exactly 4 (reproduces the known theorem) | `C`, exact, width-invariant from width 12 |
| Same quantity at `p=3`: **unbounded** for all 6 nonconstant words (checked to run-length 18 by two independent methods) | `M/C` (bounded exactly to 18; not asymptotic) |
| Same quantity at `p=4`: unbounded for 12 of 14 words; the 2 exceptions are non-primitive (secretly period 2) and reproduce period 2's bound of 4 exactly | `C` |
| Same quantity at `p=5`: unbounded for 15 of 30 words; bounded (4-7) for the other 15, **never below 4** | `C` |
| Single-isolated-one family (`0^(p-1)1`): bound is exactly `p+2` for `p=2` and `p=5..10`; **unbounded** at `p=3,4` (a clean law with a two-period exception) | `C`, width-stable 12-24 (`p=5`) and 16-24 (`p=10`) |
| Rule 90 control: the exclusion mechanism never fires for Rule 90, at any period tested; the unconstrained-survival result is identical for every period (`32768` states, stable) | `C` |
| What a genuine (not just strip-surviving) realization of the unbounded candidates would mean for R1 | `R`, honest, not claimed to be closed |

## 0. Setting, restated precisely

Write `c_t` for the centre column, assumed eventually periodic with period
`p` (word `c_0,...,c_{p-1}` repeating), and `r_t = s(t,1)` for column 1.
`PATH.md` section 2 proves, in fully general (not period-2-specific) terms:

```text
c_t = 1  =>  l_t = 1 XOR c_(t+1)                    (free, from the trace alone)
c_t = 0  =>  l_t = c_(t+1) XOR r_t                  (needs column 1)

assuming c eventually periodic:
  column -1 eventually periodic  <=>  r restricted to {t : c_t = 0} eventually periodic
```

and column `-1` eventually periodic contradicts Jen 1990 Prop. 3 / Kopra
Thm. 3.5 (no two adjacent columns both eventually periodic). Generalize
`rho`: sample `r_t` at every `t` with `c_t = 0`, in increasing time order.
For `p=2` this is exactly `RESULTS-alt-trace-fiber.md`'s `rho_k = r_(2k)`;
for general `p` the zero set is a union of some of the `p` residues mod
`p`, and this is the natural generalization already named (but not
pursued) in that same file: "The route is not period-two-specific... The
same construction runs for an arbitrary periodic centre word."

## 1. The pin: already general, reconfirmed

Nothing here is new. `PATH.md` section 2's reduction never assumes `p=2`;
it is stated for an arbitrary eventually periodic `c`. It is restated above
verbatim and used as the definition of `rho` throughout this report.

## 2. The five-zero theorem does not generalize as a uniform bound

### 2.1 The realizable-sample language: regular everywhere, finite-type only at `p=2`

`RESULTS-alt-trace-fiber.md` already derived and resolved this gap: column
1's one-step update (`s(t+1,1) = c_t XOR (s(t,1) OR s(t,2))`, with `s(t,2)`
existentially free) gives a regular language for every periodic word's
realizable-sample sequences, but **only at `p=2` is the forbidden set
finite** (`11`, `00000`); for `p=3` word `001` the minimal forbidden words
grow without bound.

Reproduced independently here (read-only import of
`experiments/rule30/alt-trace-frontier/sample_filter.py`, not edited):

```text
minimal_forbidden('001', maxlen=12):
111, 1011, 10010, 100011, 1000010, 10000011, 100000010,
1000000011, 10000000010, 100000000011
```

matching the cited pattern exactly and extending it two further terms. This
settles, independently, that the finite-type structure behind the five-zero
theorem is a `p=2` peculiarity, not a general phenomenon: for `p>=3` the
constraint is still decidable (regular) but has no finite presentation as a
short forbidden-factor list, so no five-zero-style short theorem can be
read off the same way.

### 2.2 A sharper, new question: how long a forced run of zero samples is even possible

Section 2.1's language captures *all* realizable sample sequences. A
narrower, more direct generalization of the five-zero theorem asks only
about the *longest run of consecutive zero samples*: for period 2 this run
is at most 4 (`00000` forbidden); is there an analogous finite cap for
general `p`, and does it grow or shrink?

Two independent methods answer this, both new code, both in
`experiments/rule30/r1-general-period/`:

1. **Exact exhaustive enumeration** (`zero_run_bound.py`): for a given
   centre word and light-cone width `N`, enumerate *every* possible
   initial right row (`2^N` of them, no approximation), drive Rule 30 with
   the given periodic centre-bit sequence, and find the longest achievable
   run of zero samples. This generalizes
   `right_trace_forbidden.numeric_rho`'s convention (`time & 1` as the
   period-2 centre bit) to an arbitrary period-`p` bit sequence; the file
   is new, `numeric_rho` itself is not edited.
2. **The generalized strip method** (`strip_general_p.py`, section 3
   below): a sound over-approximation, so an empty reachable set is a
   genuine proof for every width, not merely a check to some `N`.

Both methods were cross-checked against each other (word `00001`, see
table below) and agree exactly.

### 2.3 Results: never tighter, usually looser, sometimes completely open

**Regression, `p=2`:** both methods reproduce the known theorem exactly:
max run = 4, stable from width 12 through 24 (light-cone-sufficient; see
section 2.4 for why 12 is already enough).

**Single-isolated-one family**, word `0^(p-1) 1` (the most direct
generalization of `01`), swept `p = 2..10`
(`experiments/rule30/r1-general-period/survey.py`,
`single_isolated_one_family`):

```text
p:          2   3          4          5   6   7   8   9  10
max run:    4  unbounded  unbounded   7   8   9  10  11  12
```

Width-stability was checked explicitly: `p=5` gives max run 7 at every
width `12,14,16,18,20,22,24` (identical every time); `p=10` gives max run
12 at every width `16,18,20,22,24`. **For `p >= 5` this family follows
`max_run = p + 2` exactly**, matching `p=2`'s own value at `p=2` (`2+2=4`)
but strictly exceeding it for every `p>=5`. `p=3,4` are not weaker
instances of this law -- they are qualitatively different: the run is not
bounded at all (checked to run-length 18 with no sign of stopping, two
independent methods, see 2.2 and the table below).

**Full necklace sweep**, every nonconstant word of period 3, 4, 5
(`survey.py`, `necklace_sweep_p{3,4,5}`):

```text
period   words   dies (bounded)   survives (checked-unbounded)   bound range among the bounded
2          2            2                    0                      {4}
3          6            0                    6                      --
4         14            2                    12                     {4}          (the 2 are 0101,1010: secretly period 2)
5         30           15                   15                      {4,5,6,7}
```

**No word at any period `p>=3`, out of 50 distinct words tested across
`p=2..10`, produced a run bound smaller than 4.** Several produced a
strictly larger bound (up to 12 at `p=10`), and a large fraction (all of
`p=3`, most of `p=4`, half of `p=5`) produced no bound at all within the
tested range. The direction is unambiguous: **the constraint loosens, not
tightens, as `p` grows**, with `p=2` sitting at the tight extreme of every
measurement made here.

Independent cross-check of one bounded and one unbounded case, exact
exhaustive enumeration vs. the strip method:

```text
word 00001 (p=5): exhaustive max_run = 7 (widths 12..27, all identical);
                  strip method:       max_run = 7 (widths 12..24, all identical)
word 001   (p=3): exhaustive: run >= 18 achieved at width 27, still growing;
                  strip method:       genuinely stable nonzero orbit at every
                                      width 16..24 (cycle sizes grow with width:
                                      204, 341, 514, 768, 1085 at widths
                                      16,18,20,22,24)
```

### 2.4 Why width 12 (not some larger number) already settles the `p=5` case

Standard light-cone argument, used throughout this repo: `zero_run_bound.py`
needs `T = 11` original time steps to gather 9 samples for word `00001`.
Any initial-row bit beyond position `T` cannot influence any of those 9
samples (finite propagation speed 1 site/step), so width `>= T+1 = 12`
already sees everything a wider row could contribute. This was verified,
not assumed: widths `12,13,14,16,18,20,22,24` all give exactly `max_run=7`.
This makes the bounded results in this report **exact, not merely
"checked to N"**, in the same sense as the original five-zero theorem's
"second integer implementation evaluates all 512 assignments of the
nine-cell light cone" -- here the light cone is bigger (up to `2^24`
assignments checked, `2^12` already sufficient) but the exactness claim is
the same kind.

## 3. The strip method transfers cleanly

`strip_general_p.py` reuses `experiments/rule30/family-seam/strip_sets.py`'s
`micro` function **verbatim, imported, not edited or reimplemented**
(hash below). `micro(rows, phase, width, rule)` already takes `phase` as
the literal centre-bit value at one micro-step and retains both
exterior-bit choices at every step; its soundness proof (every actual right
half-plane trajectory projects into a path of the relation) never
mentioned period 2 -- it consumes one committed bit at a time, regardless
of what schedule of bits is fed to it. What `strip_sets.py`'s own `block()`
hardcodes is the *schedule*: exactly `[0, 1]` repeating. `strip_general_p.py`
replaces only that schedule with one built from an arbitrary period-`p`
word (`zero_phase_schedule`), and drives `micro` with it.

**This is demonstrated, not asserted.** Regression
(`survey.regression_against_p2_strip`, width 20): specializing the general
machinery to `p=2` and asking for the gap-2 and gap-4 stable sets
reproduces `RESULTS-family-seam.md`'s `670` and `1021` states **exactly**,
bit-for-bit (`gap2_match: true, gap4_match: true` in
`survey-results.json`), not merely matching cardinality.

Consequence: the family-seam method -- sound emptiness proofs of
specified periodic samples under an over-approximating finite-width strip
-- is now available at every period `p`, not only `p=2`. Section 2.2-2.3's
strip-based results already used it. The remaining limitation is exactly
the one family-seam always had: **survival in the strip is necessary, not
sufficient, for real realizability** (section 5).

Provenance: `experiments/rule30/family-seam/strip_sets.py` SHA-256
`aed13fead4455f055fd5eead55fb58501e6571c480ed9c177891152ff7d4e3c4`
(imported unchanged; not one of the four officially frozen engines, but
treated the same way here: read-only). `experiments/rule30/ladder/ladder.py`
SHA-256 `589ab8443e8e61a604561823335d1066eeac5d6b093800a70e8d4a1f943ff96e`,
verified unchanged (not otherwise used in this report).

## 4. Standing constraints

**Rule 90 filter.** `strip_general_p.py`'s `micro` supports `rule=90`
(inherited unchanged from `strip_sets.py`; Rule 90 has `branching = True`
unconditionally, since it has no OR-pin). Run at every period tested for
the "rho identically zero forever" question: Rule 90 shows **zero
exclusion** at `p=2,3,4,5` (state count stays at the full `32768`,
unconditionally, forever -- `rule90_controls` in `survey-results.json`).
This is the expected control: Rule 90 has no pin (`g(b,0)=g(b,1)` never
holds, `PATH.md` section 1), so it has no mechanism to exclude anything
here at any period, matching the section-0 filter's requirement that a
genuine Rule-30 mechanism must fail for Rule 90. The bounded results in
section 2.3 (the actual exclusions, e.g. `p=2` and half of `p=5`) are
Rule-30-specific by the same OR-saturation argument the original five-zero
theorem uses (`RESULTS-RIGHT-FILTERED-MORTALITY.md` section 1); this report
does not re-derive that argument, only reconfirms it transfers (the
mechanism inside `micro` is the unmodified Rule 30 truth table).

**Bounded-window closure (Theorem W).** Not violated. Nothing here predicts
an unknown `r_t` from a bounded window of `c`-history. Every claim in
section 2 concerns a **fully specified** periodic centre word, refuted (or
found to survive) by a finite strip cone or exact enumeration -- the same
side of the line the family-seam method was already on. No decision
procedure for an unknown word's eventual periodicity is proposed anywhere
in this report.

**Front lemma.** Same point stated explicitly: every exclusion here is a
refutation of one fully specified periodic word (or a demonstration that a
fully specified word survives), never a bounded-radius decision about an
unknown word's eventual periodicity. This report is on the permitted side
of the front lemma throughout.

## 5. What this does, and does not, mean for R1

**It does not close R1 or P1.** Nothing here constructs an actual infinite
(or even long finite, SAT-verified) right-half realization. The "survives"
verdicts in section 2.3 are strip-method survivals: **necessary, not
sufficient**, conditions for real realizability, exactly like every other
family-seam-style result in this repo. A surviving candidate is a candidate,
never a witness (`RESULTS-family-seam.md`'s own repeated caution, reused
here unchanged).

**Correction, 2026-09-15: the generic realizations exist; the proposed
seed inference was invalid.** Recentered versions of already recorded
space-12/time-3 and space-7/time-4 tori have `c=r=001` and `c=r=0001`,
respectively. Thus their right-neighbour samples at centre-zero times are
identically zero forever. Exact rows, source identifications and independent
local checks are in [the scope audit](RESULTS-r1-periodic-realization-scope.md#2-two-generic-right-half-realizations-already-occur-in-archive-tori).
Their reconstructed left columns are periodic, but their rows are not
left-finite, so Jen/Kopra supplies no contradiction. Existence of one such
right history also does not force the seed's right history to equal it.
This closes the unrestricted existential subtask without a larger SAT run;
it proves no lone-seed period exclusion and no zero-initial-half-line result.

**Where this leaves the programme, honestly.** The measured direction
(section 2.3) is a structural explanation for why the R1 zero-set route has
stalled exactly at `p=2`, not a search failure: `p=2` is the unique tested
case where the natural generalized quantity (longest forceable run of zero
samples) is at its tightest, and for every larger period tested it is
weakly to (mostly) unboundedly looser. This is consistent with, and adds a
sharper quantitative layer to, the existing `RESULTS-alt-trace-fiber.md`
weak-model sweep (period 2-5, "depth gained per additional one" rates
`3.6, 3.0, 1.8, 1.8` -- also not collapsing to zero but trending down) and
with R7's independent, heavier omega-automaton ladder finding NONEMPTY at
every tested `p = 2..8` (`PATH.md` section 4, `RESULTS-ladder-rung0/1.md`).
Three different mechanizations -- the weak one-step model, the Buchi
ladder, and this report's strip-based exact bound -- now agree that nothing
about periods `p=3..8` closes more easily than `p=2`; this report is the
first of the three to give an exact, width-verified numeric bound
(`max_run = p+2` for the single-isolated-one family, `p != 3,4`) rather than
a search-terminated-or-not verdict.

## 6. Reproduction

```bash
cd experiments/rule30/r1-general-period
python3 survey.py                 # ~5 seconds, writes survey-results.json
python3 zero_run_bound.py --words 001 00001 --n-samples 18 --widths 27
                                   # ~25 seconds, writes zero-run-results-rule30.json
cd ../alt-trace-frontier
python3 -c "import sample_filter as sf; print(sf.minimal_forbidden('001', maxlen=12))"
```

## 7. Scope, honesty notes

- **R1 and P1 remain open.** No claim to the contrary is made anywhere in
  this report.
- **"Survives" is never "realizable."** Every SURVIVES verdict in section
  2.3 is a strip-method necessary condition only. The companion
  `RESULTS-gap3-impossibility.md` (this session, same standing-constraint
  batch) contains a direct, checked example of a strip survivor at one
  width dying at a wider one; the survivors reported here have been checked
  at up to 5 widths and grow rather than shrink, which is suggestive but
  explicitly **not** treated as proof.
- **The necklace sweep is exhaustive only for `p = 3,4,5`.** `p=6..10` were
  checked only for the single-isolated-one family, not every necklace;
  the `p+2` law is reported as measured for that one family, not
  conjectured to hold for every word at those periods.
- **The "not yet stable" / cycle-detection check has a bounded lookback**
  (`3*z` matching entries). A survivor could in principle have a longer
  transient before settling into a cycle with period `> z`; every reported
  SURVIVES verdict here was confirmed with an explicit repeating cycle
  within the sample budget used (60-90 samples), and the flagship cases
  (`001`, `0001`, `00101`) were independently re-confirmed to length-18
  runs by the unrelated exact-enumeration method, so this risk is small
  but not eliminated by construction.
- **No claim of an asymptotic law for the DIES side beyond the single
  isolated-one family.** The `p=5` mixed necklace bounds (`4,5,6,7`) were
  measured exactly but no formula is proposed for them.
- **Every numeric claim in this report names the script that produced it**
  (`survey.py`, `zero_run_bound.py`, or the cited `sample_filter.py`), and
  every strip-method claim is exact and width-checked, not asymptotic
  extrapolation from a single width.
