# Ideomotor residual rho_k: verification of the LLM-panel spark

## Status

**KILLED**, on three independent legs, any one of which is sufficient:

1. **Vacuous by construction.** All sampled times `T+jp` share the residue
   `T mod p`, so under the periodicity hypothesis the "unlocked" gate is
   decided once, at `j=0`, not beat-by-beat. If `c_T=1`, `rho_k = 0`
   identically for every `k` -- trivially bounded, zero information about
   `r`. If `c_T=0`, `rho_k` reduces to a plain running sum of `r`'s
   stride-`p` subsequence with `c` never entering the sum again. Either way
   the "unlocked beat" / fatigue conceit that gives the spark its name
   contributes nothing (section 1). This is the same shape as the
   dendro-frost spark's section 2 ("the off-column rule enters only the
   index set, never the compared values").
2. **The rule-30-specific version is closed by the repo's own finite-prefix
   lemma.** `RESULTS-eventual-period.md`'s exact defect algebra, solved
   directly, shows `d_t(1)` (`r`'s defect) is a **free bit** at every `t`
   under the periodicity hypothesis -- not merely "no derivation was found",
   but one equation in two unknowns, solved. Independently, the same
   document's PROVED finite-prefix lemma states left permutivity supplies a
   unique left/right split with **no constraint** between a prescribed
   center trace and a compatible right-column prefix, at any finite horizon.
   So even a genuinely periodic `c` (through any finite time `N`) constrains
   nothing about `r_0..r_N` (section 2).
3. **The universal version is refuted by an existing counterexample, exactly
   (not just empirically).** Rule 90's lone-seed centre column truly is
   eventually periodic (period 1, identically 0 for `t>=1`, the fact
   `PATH.md` section 0 cites from Kopra). Running the spark's construction on
   that real orbit gives a closed form, `rho_k = 2*floor(log2(k+1)) - k`,
   proved below and matching the simulation exactly at every checkpoint
   through `k=5999`: unbounded, `Theta(-k)`, forever. A universal claim
   ("periodic implies bounded") with a proved counterexample is dead outright
   (section 3).

Together these mean: the spark's core mechanism has no content (leg 1), the
repo's existing algebra already closes the only route that could rescue a
Rule-30-specific version (leg 2), and the general form of the claim is
refuted by a theorem, not just a simulation (leg 3). This is obstruction D
(the missing composition law / unproved boundedness-by-analogy) from
`PATH.md` section 7.3, confirmed again, this time with the missing
composition law shown to be not merely absent but **empty** (leg 2) and the
general boundedness claim shown **false** (leg 3).

`rho_k` does pass the standing single-column-sensitivity filter (`PATH.md`
0.1) in the sense that overwriting column 0 changes the gate and hence moves
`rho_k` -- worth stating precisely, because it means this kill had to come
from elsewhere (it did: legs 1-3 above), not from filter 0.1.

Code:
`experiments/overnight-arms/roundtable_followup3/ideomotor_residual/residual_probe.py`
(read-only reuse of `evolve_rows`/`cell` from
`experiments/rule30/periodicity_bridge_probe.py`).
Raw output:
`experiments/overnight-arms/roundtable_followup3/ideomotor_residual/residual_probe_results.json`
in the same directory.

## 1. Making rho_k precise

As specified in the task, fix a candidate period `p` and start time `T` for
`c_t = s(t,0)`, and track `r_t = s(t,1)`. Define, summing only over "unlocked"
beats where the *assumed* period's centre value reads zero:

```text
rho_k = sum_{j=0}^{k-1} (1 - c_{T+jp}) * (2*r_{T+jp} - 1)
```

**Vacuity leg (Status item 1).** If `c` really is exactly `p`-periodic from
time `T` onward, then every sampled time `T+jp` shares the **same residue**
`T mod p`, so `c_{T+jp} = c_T` for every `j` -- the "unlocked" condition is
either true for *all* `j` or false for *all* `j`, decided once, at `j=0`.
There is no phase variation across `j` to track. Concretely:

* If `c_T = 1`: every beat is locked, `(1-c_{T+jp})=0` for all `j`, and
  `rho_k = 0` identically for every `k`. Trivially bounded, and carries zero
  information about `r`.
* If `c_T = 0`: every beat is unlocked, and `rho_k` reduces to a plain
  running sum of `(2*r_{T+jp}-1)` over the single-phase subsequence
  `r_T, r_{T+p}, r_{T+2p}, ...`, with `c` never entering the sum again after
  deciding this one bit.

Either way, the "unlocked beat" / fatigue-oscillator conceit -- the entire
ideomotor framing -- does no work: the quantity collapses to either the
constant `0` or an unconditional sum over `r`'s stride-`p` subsequence. What
remains, in the nonvacuous case, is exactly this repo's already-open R1
target ("periodic centre implies periodic (or otherwise `p`-predictable)
adjacent column", `RESULTS-eventual-period.md` line 52-55, "No such
derivation survived the tests below"), reached with no new mechanism.

## 2. Re-deriving what periodicity of c actually implies about r

`RESULTS-eventual-period.md` already proves the exact Rule 30 defect
recurrence. Writing `d_t(x) = s(t+p,x) XOR s(t,x)`:

```text
d_(t+1)(x) = d_t(x-1) XOR d_t(x) XOR d_t(x+1)
             XOR s(t,x) d_t(x+1) XOR s(t,x+1) d_t(x)
             XOR d_t(x) d_t(x+1)
```

Under the hypothesis that `c` has become exactly `p`-periodic
(`d_t(0)=d_{t+1}(0)=0`), this **PROVED** reduction holds:

```text
d_t(-1) = (1 XOR c_t) AND d_t(1)
```

`d_t(1) = r_{t+p} XOR r_t` is exactly `r`'s own defect under the shift `p` --
the object `rho_k`'s drift is a running, signed accumulation of.

**One-line proof that this identity constrains `r`'s defect not at all
(Status item 2, first half).** Go one step before the "reduces to" in
`RESULTS-eventual-period.md`: the raw `x=0` instance of the general defect
recurrence, under the assumption `d_t(0)=d_{t+1}(0)=0` that produces the
displayed identity, is

```text
0 = d_t(-1) XOR d_t(1) XOR c_t . d_t(1)
```

one equation in the two unknowns `d_t(-1)` and `d_t(1)`. Solving it for
`d_t(-1)` gives the displayed identity; solving it for `d_t(1)` is not
possible without already knowing `d_t(-1)` -- the equation has one degree of
freedom, and nothing else in the periodic-centre hypothesis pins it down.
`d_t(1)` (`r`'s defect) is therefore a **free bit** at every `t` consistent
with `c_t = c_{t+p}` and `c_{t+1}=c_{t+1+p}`: the hypothesis constrains the
*relationship* between `l`'s defect and `r`'s defect, never `r`'s defect on
its own. This is not "no derivation was found" (a negative); it is one
equation in two unknowns, solved, with the free variable identified.

**Independent confirmation from a result already proved in the same source
document (Status item 2, second half).** `RESULTS-eventual-period.md`'s
**PROVED finite-prefix lemma** states: for any finite desired centre trace
`tau_0,...,tau_N` and any compatible right prefix `R_0,...,R_N`, left
permutivity supplies a unique left column `L_1,...,L_N` matching it -- i.e.
prescribing the centre trace through time `N` (in particular, a periodic
one) imposes **zero constraint** on the right prefix `R_0,...,R_N`, because
the right prefix is free to be anything and a compatible left column always
exists. Applied here: fixing `c`'s trace to be periodic through any finite
horizon `N` leaves `r_0,...,r_N` completely unconstrained by that
prescription. This closes off any *local or finite* mechanism by which
periodicity of `c` could bound `r`'s stride-`p` sum -- and a "fatigue
oscillator" is exactly such a local, finite-state mechanism (it accumulates
one signed bit per beat with no other memory). The honest caveat: this is a
finite-horizon statement, so it does not by itself formally exclude a
constraint that only emerges in an asymptotic (`N -> infinity`) limit: but
that would require a genuinely new argument this repo does not have, and is
exactly the R1 target flagged as open, not something the spark supplies.

Together, this is exactly the shape of obstruction D in `PATH.md` 7.3: a
composition law is needed (here, one that would pin `d_t(1)`, hence `r_t`'s
long-run behavior, from `c`'s periodicity) and this section shows it is not
merely missing but **empty** -- one equation short by construction (first
half) and independently ruled out at every finite horizon by a lemma the repo
already proved (second half). The "fatigue oscillator" analogy asserts
boundedness without supplying, and in the face of, this missing law.

**Re-verification on the real orbit** (`defect_identity_reverification` in
the JSON output): restricting to times in the real Rule 30 lone-seed orbit out
to `t=6000` where `c` *locally* happens to satisfy `d_t(0)=d_{t+1}(0)=0` for
trial `p in {2,3,4}` (a coincidental local match, not a claim of global
periodicity), the identity holds with **zero exceptions** across every tested
case:

| `p` | cases tested | identity held |
|---:|---:|---:|
| 2 | 1466 | 1466 |
| 3 | 1498 | 1498 |
| 4 | 1554 | 1554 |

This reproduces `RESULTS-eventual-period.md`'s proof exactly (as it must --
it is the same identity), and confirms the harness is wired correctly. It
adds no new constraint on `r`, because, as derived above, the identity was
never capable of supplying one.

## 3. The decisive counterexample: Rule 90's TRUE period

Rather than rely only on "no derivation exists" (a negative, and per this
program's discipline a negative result needs to be an honest failure-to-find,
not proof of impossibility), item 2 of the task asks for a direct check
against the real orbit. The strongest available version of that check is to
apply the *identical* construction to a case where the periodicity premise is
not hypothesized but **actually true**: Rule 90's lone seed.

`residual_probe.py` simulates the Rule 90 lone seed to `t=6000` and confirms
the standard fact directly (`rule90_center_check` in the JSON): `c_t = 0` for
every `t` from `1` to `6000` with zero exceptions -- Rule 90's centre column
is eventually periodic with true period `p=1`, starting at `T0=1`, exactly as
`PATH.md` section 0 states from Kopra.

Under this *true* period, every beat `t>=1` is unlocked (`c_t=0` always), so
`rho_k` reduces to the plain running sum of `(2*r_t-1)` over Rule 90's own
`x=+1` column, `t=1..k`. Result (`rule90_true_period_rho`, `T0=1`, `p=1`,
`k_max=5999`):

| `k` | rho_k | rho_k / k |
|---:|---:|---:|
| 10 | -4 | -0.400 |
| 50 | -40 | -0.800 |
| 100 | -88 | -0.880 |
| 500 | -484 | -0.968 |
| 1000 | -982 | -0.982 |
| 2000 | -1980 | -0.990 |
| 5000 | -4976 | -0.995 |
| 5999 | -5975 | -0.996 |

`rho_k` does not stay bounded. It drifts essentially linearly at a rate
converging to `-1` per beat.

**Exact closed form, not just a measurement.** Rule 90's `x=1` column is the
second diagonal of Pascal's triangle mod 2: `r_t=1` iff `t=2m+1` is odd and
`C(2m+1,m+1)` is odd, and by Kummer's theorem `C(2m+1,m+1)` is odd iff adding
`m` and `m+1` in binary carries nowhere, i.e. iff `m AND (m+1) = 0`, i.e.
`m in {0} union {2^k - 1 : k>=1}`. So `r_t = 1` **exactly** at
`t = 2^j - 1` for `j = 1, 2, 3, ...`, and `r_t = 0` at every other `t >= 1`.
Checked directly against the simulated array: the sole `t<=6000` with
`r_t=1` are `{1,3,7,15,31,63,127,255,511,1023,2047,4095}` -- precisely
`{2^j-1 : j=1..12}` -- matching the measured `num_ones_in_r_among_unlocked:
12` exactly, not approximately. Since `T0=1, p=1`, `rho_k = (2 . #{j>=1:
2^j-1 <= k}) - k = 2*floor(log2(k+1)) - k`. This closed form reproduces
every checkpoint in the table above exactly (verified by direct computation,
not curve-fitting) and proves, for all `k`, `rho_k = -k + O(log k) ->
-infinity`. **Unboundedness here is a theorem, not a finite-window
observation that might turn around later.**

**This is a direct, existing counterexample to the universal form of the
spark's central premise.** That premise, read as a universal claim over
rules and periods -- "IF c is eventually periodic with period p, THEN rho_k
stays bounded", with no reference to which rule produces `c` -- has Rule 90
as an instance where the antecedent is true (proved) and the consequent is
false (proved). One counterexample refutes a universal claim. This does not,
by itself, kill a Rule-30-specific restatement of the premise (a claim only
about Rule 30's own `c` and `r`) -- Rule 90 is silent on that narrower claim
by definition, since it is a different rule. The Rule-30-specific version is
closed separately, in section 2 above (the finite-prefix lemma and the
free-bit argument), not by this section. Both legs are needed; each kills a
different scope of the claim.

## 4. Rule 90 filter, explicitly

Per the task's item 2 and this program's core filter (`PATH.md` section 0):
does the mechanism care whether the underlying rule is 30 or 90? Section 3's
result answers this directly and more strongly than usual -- it is not merely
that the mechanism "also applies" to Rule 90 in a way that would prove
something false; the mechanism, run verbatim on Rule 90, demonstrates that
its own premise is false in a case where the periodicity hypothesis is
*known true*. This is a stronger form of the standard filter failure: most
killed routes in this program's history "prove too much" on Rule 90 (would
falsely certify something); this one instead shows the mechanism's load-
bearing lemma ("periodicity bounds rho") is simply wrong, using Rule 90 as
the cheapest available place to exhibit true periodicity and check the
consequence.

## 5. Rule 30's real orbit and the constructed-periodic-diagram question

For completeness (task item 1, second half): can column 0 even be
consistently embedded as eventually periodic in a full Rule 30 diagram, and
if so what does `r` look like there? This is exactly the object
`experiments/rule30/eventual_period_probe.py` already searches for via exact
SMT enumeration (`RESULTS-eventual-period.md`, "Incremental exact search").
That search finds only **finite** periodic-centre prefixes before UNSAT (for
example the row `{-1}` matches `(01)^infinity` only through `t=6`; the
largest horizon found across the swept radii/periods is `t=17`). No infinite
consistent embedding of a nonconstant periodic centre is known to exist --
constructing one is exactly Prize Problem 1, not a side question this task
can resolve by re-running that search. Re-running the existing SAT harness
here would not add information beyond what `RESULTS-eventual-period.md`
already reports, so it is cited rather than duplicated.

What the real (unproven, presumably non-periodic) Rule 30 orbit does, purely
descriptively (`rule30_trial_periods` in the JSON, trial periods
`p in {2,3,4,6,8}`, three start times each, `k<=400`): `rho_k` stays small,
`|rho_k| <= 29` throughout, consistent with `O(sqrt(k))` random-walk-scale
noise over a few hundred samples of a locally uncorrelated-looking
`{-1,+1}` sequence. There is a sharper, structural reason this carries **no
evidential weight**, beyond "small sample": `num_unlocked` in these runs sits
around 190-214 out of `k_max<=400`, i.e. the gate is *varying* across `j`
within each run. By section 1's vacuity argument, a genuine period `p` forces
the gate to be constant (all-unlocked or all-locked) for the entire run. A
varying gate is direct evidence that `c` is **not** exactly `p`-periodic at
this trial `p` over this window (as expected -- these are guessed trial
periods on an orbit not known to be periodic at all), which means these runs
are not even computing `rho_k`-under-the-hypothesis as specified; they are
computing a related but different statistic (a gated sum against a *false*
candidate period). It is reported only to show the harness was exercised
against the real orbit as the task asked, not to found any conclusion on it.

## Verdict

**KILLED**, on three independent legs (Status block above), restated with
scope made explicit:

1. **Vacuous by construction (section 1), all scopes.** Under the
   periodicity hypothesis the unlocked gate is decided once by `c_T`, not
   beat-by-beat: `c_T=1` forces `rho_k=0` identically (zero information),
   `c_T=0` reduces `rho_k` to an unconditional sum with the gate never
   re-entering. The "fatigue"/"unlocked beat" framing does no work in either
   case.
2. **Rule-30-specific version of the premise, closed (section 2).** The raw
   `x=0` defect equation, solved directly, has `d_t(1)` (`r`'s defect) as a
   free bit -- not "no derivation found", one equation in two unknowns,
   solved. Independently, `RESULTS-eventual-period.md`'s already-proved
   finite-prefix lemma shows a periodic centre trace constrains the right
   column not at all at any finite horizon. Together these close off any
   local, finite-state mechanism (which a fatigue oscillator is) by which
   `c`'s periodicity could bound `r`'s stride-`p` sum, for Rule 30
   specifically.
3. **Universal version of the premise, refuted by a proved counterexample
   (section 3).** Rule 90's lone-seed centre column is truly eventually
   periodic (period 1, verified exactly to `t=6000`), and its `rho_k` has
   the exact closed form `rho_k = 2*floor(log2(k+1)) - k -> -infinity`,
   proved via Kummer's theorem on the Pascal-triangle-mod-2 structure of its
   `r`-column, not merely measured. A universal "periodic implies bounded"
   claim, refuted by a proved instance, is dead; this leg does not by itself
   speak to the Rule-30-specific claim (leg 2 does that).
4. **Rule 90 filter (`PATH.md` section 0), in a stronger-than-usual form.**
   The mechanism, run unmodified on Rule 90's true period, does not just
   "fail to discriminate" -- it falsifies its own core lemma outright in a
   case where the hypothesis is known true, using the standing filter's own
   test case.
5. Whether column 0 can even be consistently embedded as eventually periodic
   in an infinite Rule 30 diagram is exactly Prize Problem 1 and is not
   resolved, established, or advanced by this construction; the existing
   exact SAT search (`RESULTS-eventual-period.md`) already reports the
   relevant finite-horizon data and is cited rather than duplicated.
6. The real Rule 30 orbit's `rho_k` under several trial (guessed, not known
   real) periods stays small over short windows, but the gate itself varies
   across those runs, which means -- per leg 1's own vacuity argument -- they
   are not even computing `rho_k`-under-the-periodicity-hypothesis; this is
   reported as harness exercise, not evidence.

This route does not advance P1, P2, or P3. Nothing about it should be
retried without first supplying the missing composition law that section 2
shows does not merely go unfound but is algebraically absent: an actual
derivation (not an analogy) that periodicity of `c` constrains `r`'s
long-run sum, surviving both the free-bit argument and the finite-prefix
lemma above.

## Reproduction and spending

```bash
cd experiments/overnight-arms/roundtable_followup3/ideomotor_residual
uv run python residual_probe.py
```

Runtime: under 5 seconds. Self-contained apart from one read-only import of
`experiments/rule30/periodicity_bridge_probe.py`. Modal: **$0**. Paid
model-provider calls: **$0**.
