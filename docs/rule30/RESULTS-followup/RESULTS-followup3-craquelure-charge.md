# Craquelure-charge defect field D(t,x): verification of the LLM-panel spark

Status: **KILLED**, but not for the reason the triage's own kill condition
(b) anticipated. Part (a) of the pre-registered kill condition is **TRUE and
confirmed exhaustively**: D does not obey an autonomous local rule for
Rule 30, and does for Rule 90 — a genuine, clean, non-hand-wavy Rule-30
versus Rule-90 discriminator. But the candidate is **not** "one definitional
step from `gauge_holonomy`" as triaged. Once the vague spark text is made
precise, the "signed stratigraphic charge" is not identically zero (it is
nonzero in 24/64 exhaustive cases below, unlike `kappa` in
`RESULTS-followup2-gauge-holonomy.md`, which was 0/32). It turns out instead
to be **an exact renaming of a quantity this repo already has: the "PROVED
run-of-ones wedge" in `RESULTS-eventual-period.md`.** That result is real,
correct, and already on record as insufficient — it gives only a bounded
wedge (because the charge is *created and destroyed*, not conserved: any
center-column `1` annihilates it), never a global contradiction. So the
craquelure-charge route dies the same death that quantity already died,
under a different name, not by triviality (gauge-holonomy's failure mode)
and not by vacuity on Rule 90 (comma-winding's failure mode).

Code:
`experiments/overnight-arms/roundtable_followup3/craquelure_charge/craquelure_probe.py`.
Raw output: `craquelure_probe_results.json` in the same directory.

## 1. Making D, the OR-gate tagging, and the "charge" precise

The spark asks for two spacetime diagrams `a` (true lone-seed) and `a'`
(agrees with `a` up to some time, then follows an assumed period-`p` center),
compared via `D(t,x) = a(t,x) XOR a'(t,x)` over the *entire* diagram, with
"OR-gate transition tags" on disagreement sites and a "signed stratigraphic
charge" that a conserved-charge argument would forbid from being globally
consistent back to a single seed.

**The charitable, checkable reading.** "`a'` follows a period-`p` pattern
after some time" only pins down `a'` as *some* full two-sided Rule 30
configuration whose center column agrees with `a`'s up to time `t` and is
exactly periodic thereafter — `a'` must still obey the real Rule 30 update
everywhere off column 0 for `D` to be a well-defined diagram at all (the
spark does not get to also assume `a'`'s off-center cells; those are
determined by requiring `a'` to be a genuine Rule 30 orbit). This is *not* a
new object: it is exactly `RESULTS-eventual-period.md`'s setup, restated.
There, for a finite configuration `x` with eventually `p`-periodic center
starting at time `T`, `y = F^T(x)` and `F^p(y)` are *both real Rule 30
orbits of finite configurations* whose center traces agree for all `t >= 0`
iff the eventual periodicity holds. Setting `a_t := F^t(y)`,
`a'_t := F^t(F^p(y)) = F^{t+p}(y)` recovers exactly this candidate's `a, a'`
pair, and

```text
D_t(x) := d_t(x) = s(t+p,x) XOR s(t,x)
```

is that document's own defect field, verbatim. This is the most faithful
formalization available, not a strawman weakening — it is required by "both
diagrams must be real Rule 30 evolutions," which the spark's own request for
"disagreement arcs" (a spacetime *structure*, not just a boundary condition)
presupposes.

**Deriving D's update rule (this report's own derivation, then checked by
exhaustive enumeration and by direct simulation below).** For any rule
`forward(l,c,r)`, `D_{t+1}(x) = forward(a_t(x-1),a_t(x),a_t(x+1)) XOR
forward(a'_t(x-1),a'_t(x),a'_t(x+1))`. Writing `OR(p,q) = p XOR q XOR pq` and
substituting `a' = a XOR D` gives, for Rule 30 (`forward = l XOR (c OR r)`):

```text
D_{t+1}(x) = D_t(x-1) XOR D_t(x) XOR D_t(x+1)
             XOR a_t(x)*D_t(x+1) XOR a_t(x+1)*D_t(x) XOR D_t(x)*D_t(x+1)
```

which is exactly `RESULTS-eventual-period.md`'s recurrence for `d_(t+1)(x)`
(there stated for the periodic-defect special case; here re-derived as a
general identity holding for *any* two Rule 30 orbits, periodicity or not —
confirming it is the right object). For Rule 90 (`forward = l XOR r`, no `c`
term at all):

```text
D_{t+1}(x) = D_t(x-1) XOR D_t(x+1)
```

**The OR-gate tag / "charge."** The three extra terms in the Rule 30
recurrence beyond the Rule-90-shaped linear part
(`D_t(x-1) XOR D_t(x) XOR D_t(x+1)`) are exactly the contribution of the
OR-gate's nonlinearity — the piece that exists only because Rule 30 has an
OR where Rule 90 has nothing. Define the **signed stratigraphic charge**

```text
kappa(t,x) := a_t(x)*D_t(x+1) XOR a_t(x+1)*D_t(x) XOR D_t(x)*D_t(x+1)
```

so that `D_{t+1}(x) = D_t(x-1) XOR D_t(x) XOR D_t(x+1) XOR kappa(t,x)`. This
is the most literal reading of "which OR-gate transition produced the
disagreement": it is precisely the extra AND/product terms that appear only
because the update is `l XOR (c OR r)` and not `l XOR c XOR r`.

## 2. Part (a): D's autonomy, exhaustive + simulated

`exhaustive_recurrence_check` enumerates the full determining footprint —
`(D_t(x-1), D_t(x), D_t(x+1), a_t(x), a_t(x+1))`, 32 cases, doubled to 64 to
also confirm `a_t(x-1)`'s absolute value is a spurious variable already
integrated out of `D_{t+1}(x)` (it only enters via its XOR-partner
`D_t(x-1)`, verified: 64/64 cases give an unchanged `D_{t+1}(x)` when
`a_t(x-1)` flips with `D_t(x-1)` held fixed).

Result (`craquelure_probe_results.json`):

| rule | `D_{t+1}(x)` a function of `(D_t(x-1),D_t(x),D_t(x+1))` alone? | matches `linear XOR kappa` |
|---|---|---|
| Rule 30 | **False** (`autonomous_in_D_alone: False`) | 64/64 |
| Rule 90 | **True** (`autonomous_in_D_alone: True`) | n/a (Rule 90 has no `kappa` term; its own linear formula `D_t(x-1) XOR D_t(x+1)` matches by direct derivation above) |

For Rule 90 this is the standard superposition fact for additive/linear CA,
confirmed here computationally rather than assumed: fixing
`(D_t(x-1),D_t(x),D_t(x+1))` and varying the underlying `a` values never
changes `D_{t+1}(x)`. For Rule 30, the same fixed `D`-triple produces both
`D_{t+1}(x)=0` and `D_{t+1}(x)=1` outcomes depending on the actual `a_t(x)`,
`a_t(x+1)` values — `D` genuinely does not evolve as an autonomous CA; it
needs the host orbit.

`random_orbit_pair_check` confirms the closed-form recurrence end to end
against literal forward simulation on 800 random 60-cell orbit pairs for
each rule, at every interior site, both rules: **0/800 mismatches**. This is
not new information beyond the exhaustive proof (which already covers every
possible local case), but it confirms the harness and the formula agree with
actual `evolve_row` simulation with no shortcuts taken.

**Part (a) verdict: TRUE, exhaustively proved, and genuinely useful as a
discriminator** — this is a real algebraic asymmetry between Rule 30 and
Rule 90 (Rule 90's difference field is itself a Rule 90 orbit; Rule 30's is
not a self-contained dynamical system at all), not a hand-wavy one. It
survives independent re-derivation and both an exhaustive and a simulated
check.

## 3. Part (b): is the charge identically zero, sign-indefinite, or something else?

`kappa` is **not** identically zero: nonzero in **24 of 64** exhaustive
cases (`rule30_kappa_properties.kappa_nonzero_cases`). This already
distinguishes the outcome from `gauge_holonomy`'s `kappa`, which was 0/32
identically by the definitional argument in that report (Path A and Path B
being the same map read forwards/backwards). Here there is no such
definitional collapse: `kappa` is a real, nonzero function of the orbit,
confirmed to genuinely depend on the actual `a` values for fixed `D`
(`kappa_varies_with_a_for_fixed_D: True`) — consistent with, and the same
underlying fact as, part (a)'s non-autonomy.

**But it is not a conserved charge, and the mechanism that breaks
conservation is exactly the one already on record.** `center_reduction_check`
exhaustively enumerates every case consistent with the standing hypothesis
that the two orbits still agree exactly at the center column at both `t` and
`t+1` (`D_t(0) = D_{t+1}(0) = 0` — i.e., no disagreement has yet appeared;
this is the regime any "forbids periodicity" argument needs to hold
*forever*, not just at one instant). Of the 16 possible input combinations,
8 are self-consistent with that hypothesis, and in **all 8 of 8**:

```text
D_t(-1) = (1 XOR a_t(0)) AND D_t(1)      [identical to RESULTS-eventual-period.md]
kappa(t,0) = a_t(0) AND D_t(1)            [the charge IS the erasure term]
```

This is the exact "PROVED run-of-ones wedge" already in the repo, not merely
similar to it: `kappa` at the center site is, bit for bit, the term that
erases an incoming defect whenever the center bit is 1 (`a_t(0)=1` forces
`D_t(-1)=0` regardless of `D_t(1)`), and passes it through unchanged whenever
`a_t(0)=0`. A "conserved charge" in the sense the spark wants (accumulates
without bound, forcing a global contradiction against a finite seed) would
require `kappa` to never be annihilated. It is annihilated by construction
every time the center hits 1.

`wedge_reach_simulation` confirms this is not merely a one-step fact but
caps the entire leftward defect-arc length at the period word's own
structure, even under an adversarial input that injects a fresh defect
(`D_t(1)=1`) at *every* single time step from the free right-hand side:

| period word | longest zero-run in one period | max defect-arc run observed (depth up to 400, adversarial injection) |
|---|---|---|
| `(0,1)` | 1 | 1 |
| `(0,0,1)` | 2 | 2 |
| `(0,1,0,0,1)` | 2 | 2 |
| `(0,0,0,0,0,0,1)` | 6 | 6 |

In every case the observed maximum equals the period word's longest run of
zeros exactly, confirming the bound is tight and structural, not an
artifact of a weak adversary: no amount of freely-chosen right-hand-side
defect injection lets an arc survive longer than the next `1` in the
assumed period.

**Classification against the triage's three-way test.** This is neither
(i) identically zero by algebraic identity (that is `gauge_holonomy`'s
outcome, not this one — `kappa` is genuinely nonzero and genuinely
non-autonomous), nor is it quite (ii) as originally imagined ("leaks
laterally"): the mechanism found is *temporal* annihilation by any center-`1`
site, not spatial leakage. But the effect is the same as (ii)'s intended
kill: **no forced net accumulation.** A nonconstant periodic word has a
bounded run of zeros by definition (period `p` implies a `1` at least once
every `p` steps unless the word is constant, which is separately excluded
by the all-one-fiber theorem in the same document), so the charge can never
exceed that bound — which is finite and independent of how far in time or
how large the assumed period `p` is tested. This is precisely (ii)'s
"charge leak... without any net accumulation forced," realized via erasure
rather than lateral cancellation, and it is the same conclusion
`RESULTS-eventual-period.md` already reached and labeled explicitly:
"a nonconstant periodic word has bounded one-runs, so this gives only a
bounded wedge, not a descent to contradiction."

## 4. Rule 90 screen

Rule 90 has no OR gate, so `kappa` (defined as the OR-nonlinearity's
correction term) does not correspond to anything in Rule 90's actual update;
Rule 90's true `D`-recurrence is the fully linear
`D_{t+1}(x) = D_t(x-1) XOR D_t(x+1)`, confirmed autonomous in section 2.
Unlike `comma_winding`'s vacuous Rule 90 pass (no s-type steps exist at
all, so the invariant is trivially 0 with no comparable quantity on the
Rule 90 side), **this pass is a genuine, non-vacuous discriminator**: Rule
90 has the same two-orbit-difference object `D`, it is well-defined and
nonzero in general, and it provably *is* an autonomous Rule-90 orbit itself
(the standard superposition principle for additive CA, confirmed
computationally here) — a meaningful, checkable fact that fails for Rule 30.
Part (a) is a real Rule 30/Rule 90 asymmetry, not a category error against a
control that doesn't have the concept.

## 5. Does this route survive?

No, but for a reason distinct from either precedent report:

* It is not killed by the gauge-holonomy pattern (identity-zero by
  definitional necessity) — the charge is genuinely nonzero and genuinely
  needs the underlying orbit, confirmed exhaustively.
* It is not killed by the comma-winding pattern (vacuous on the Rule 90
  control) — the Rule 90 comparison is real and the asymmetry in part (a)
  is a legitimate discriminator.
* It is killed because, once precisely formalized, the "conserved charge"
  is **exactly** `RESULTS-eventual-period.md`'s already-proved run-of-ones
  wedge, and that result's own stated limitation applies verbatim: bounded
  by the period word's zero-runs, hence never forced to grow, hence no
  descent to a global contradiction against the finite seed. This is
  obstruction analogous to D in `PATH.md` section 7.3 in spirit (a real
  local identity that does not close globally) but is more precisely a
  **duplicate of already-catalogued material**, not a new instance of
  obstruction D's missing-composition-law pattern.

**What would be needed for this to survive:** a mechanism that forces
`kappa` (or some other charge derived from the same `D`-recurrence) to
accumulate *across* the erasure events rather than being reset by them —
e.g. a charge defined so that a center-`1` site converts rather than
destroys it, or a charge tracked on a different variable than the raw
defect run-length. No such mechanism was found, and `RESULTS-eventual-period.md`
already records that no such derivation survived its own tests (the same
statement holds here for the identical underlying object). Absent that,
this is the same wall under yet another name.

## Verdict

**KILLED** on independent re-derivation, not on the triage's pre-registered
framing verbatim:

1. Part (a) (autonomy asymmetry) is **TRUE**, exhaustively proved (64/64
   footprint cases both rules, matching a from-scratch algebraic
   derivation, confirmed further by 1600 simulated random-orbit-pair
   checks with 0 mismatches) — a genuine, non-hand-wavy Rule 30/Rule 90
   discriminator that survives as a true fact.
2. Part (b) does **not** collapse the way `gauge_holonomy` did — the
   charge is not identically zero for either rule by algebraic necessity.
   It is instead a verbatim restatement of `RESULTS-eventual-period.md`'s
   already-proved run-of-ones wedge (`d_t(-1) = (1 XOR c_t) AND d_t(1)`,
   confirmed here exhaustively as the unique consistent solution in all 8
   of 8 applicable cases, with `kappa(t,0) = c_t AND d_t(1)` identified as
   the erasure term), whose own documented limitation — bounded by the
   period word's longest zero-run, hence no forced accumulation — applies
   here without modification.
3. The triage's framing ("one definitional step from `gauge_holonomy`") is
   **not correct**: this candidate is closer to, and turns out to be
   identical in content to, the `RESULTS-eventual-period.md` machinery, a
   third precedent not named in the triage brief. The two failure modes
   (gauge-holonomy's identity-zero triviality; this one's real-but-bounded
   non-conservation) are different, and conflating them would have missed
   that part (a) is a genuinely true and useful fact that simply isn't
   sufficient on its own.
4. No part of this route advances P1, P2, or P3. It should not be retried
   under the "conserved charge" framing without a concrete mechanism that
   defeats the erasure-by-ones bound already measured — the same
   requirement `RESULTS-eventual-period.md` already states as its open
   remaining obligation.
