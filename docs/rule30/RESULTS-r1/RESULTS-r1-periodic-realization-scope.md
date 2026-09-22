# R1: a pin counterexample, existing periodic realizations, and a mismatch bound

Date: 2026-09-15. **P1 and its nonconstant-period exclusions remain open.**
This audit separates three statements that the older route descriptions
do not consistently distinguish. It also extracts a quantitative corollary
of the existing driven-left-half-plane proof. No new torus family is claimed.

The [checker](../../experiments/rule30/r1_periodic_realization_scope_audit.py)
and [artifact](../../experiments/rule30/r1-periodic-realization-scope-audit.json)
retain the exact examples and bounded independent controls.

## 1. The literal PIN-Pi conjecture has a two-test counterexample

Let `LHP_0(c)` be the driven left half-plane with all negative spatial
cells initially zero, prescribed boundary `s(t,0)=c_t`, and the Rule 30
equation imposed at every `x<=-1`. Write `l_t=s(t,-1)`. Its centre pin is

```text
c_t=1  =>  l_t = 1 XOR c_(t+1).                           (PIN)
```

The [direct LHP proof, section 5(b3)](../../experiments/rule30/p1-period2-invariant/uc/r1-r1zero-prove-driven-lhp-column-minus-one-aperiodic-direct/PROOF.md)
defines PIN-Pi as: no eventually periodic `c` with `c_0=1` makes this
zero-initial LHP satisfy PIN at every time. **That literal statement is
false**, rather than open. Take

```text
c = 1,1,0,0,0,... .
```

The driven LHP has `l_0=0` and `l_1=1`. Its only nonvacuous pin tests are
at times zero and one, and they are respectively `0=1 XOR 1` and
`1=1 XOR 0`. At every later time `c_t=0`, so PIN asks nothing.

This boundary does not satisfy the centre equation after adjoining the
zero-initial driven right half-plane. At time two its neighbours are
`l_2=1`, `r_2=0`, while `c_2=0`. Rule 30 requires `c_3=1`, whereas the
prescribed value is zero. The first glue failure is therefore the update
at time two.

More generally, a genuine centre prefix ending at a zero can be continued
by zeros forever. All earlier pin tests remain satisfied by temporal
causality, and no later ones occur. This is not an actual-orbit extension:
the zero-time coupling to the driven right half-plane remains unverified.

The existing [constant-tail exclusions](RESULTS-eventual-period.md) remain
valid in their full-diagram scope. A repaired pin-only target must restrict
to nonconstant eventual tails, treating the constant cases separately.
This audit neither proves nor refutes that repaired target. The structural
LHP proof's corresponding open-horn discussion has the same literal
constant-tail issue; its aperiodicity theorem is unaffected.

## 2. Two generic right-half realizations already occur in archive tori

The [general-period report, section 5](RESULTS-r1-general-period.md) names
the existence of an actual right-half realization with zero samples under
drives `001` and `0001` as an unattempted subtask. Both occur by choosing
a different observed column in existing, forward-verified tori.

Each string below is a whole spatial period, with column zero first.
Rows repeat cyclically in time and spatially in both directions.

```text
Centre and right column both 001, spatial period 12:
000100111110
001111100001
111000010011

Centre and right column both 0001, spatial period 7:
0000100
0001110
0011001
1110111
```

All 36 and 28 local updates, including the final-to-first row, satisfy
Rule 30. In each example `r_t=c_t`, so the chronological right-neighbour
samples at centre-zero times are identically zero for all time.

These are **not newly discovered tori**. The first is spatial shift ten
of the torus in [the c=011 seam report, section 4](RESULTS-r1-c011-seam.md).
The second is spatial shift two of the space-seven/time-four torus in
[the alternating-fibre report](RESULTS-alt-trace-fiber.md). The checker
compares all rows under those shifts, in addition to independently
checking the rule through Boolean arithmetic and the Wolfram truth table.

This closes the named generic existential subtask, but neither initial
right half is all zero. Both full rows have infinitely many ones to the
left. Thus these witnesses do not address the zero-initial driven
half-line, finite-seed reachability, or the lone seed.

The proposed downstream inference in the general-period report is invalid:
one such realization does not make that centre word impossible for the
lone seed. A witness with two periodic adjacent columns is outside the
nonzero left-finite universe of the width-two theorem. Moreover existence
of one right history never forces the seed's particular right history to
be that witness.

The left-finite obstruction can also be seen without invoking an external
theorem. If two adjacent columns of a nonzero left-finite diagram are
eventually `P`-periodic from a common onset, the inverse Rule 30 equation
propagates that same period and onset to every column on their left.
But the leftmost one advances one site left per step. At a sufficiently
late time `T`, its position at `T+P` is zero at time `T` and one at time
`T+P`, contradicting that propagated periodicity. Tori have no leftmost
one and therefore do not meet this argument's hypothesis.

## 3. A quantitative corollary of the driven-LHP edge proof

The [existing direct proof, section 3](../../experiments/rule30/p1-period2-invariant/uc/r1-r1zero-prove-driven-lhp-column-minus-one-aperiodic-direct/PROOF.md)
shows that a nondegenerate finite-left driven half-plane cannot have both
boundary and adjacent column eventually periodic. The following explicit
finite-interval consequence uses the same mechanism; it is a quantitative
corollary, not a new mechanism for proving P1.

Use `LHP_0(c)` as above, assume `c_0=1`, and let `T>=0`, `P>=1`. If

```text
c_(u+P)=c_u  for T <= u <= 2T+P-2,                       (1)
```

then there exists

```text
t in [T,2T+P-1] with l_(t+P) != l_t.                     (2)
```

An interval with upper endpoint below its lower endpoint in (1) is empty.

**Proof.** Put `J=T+P>=1` and suppose no mismatch occurs in (2). The
inverse equation, valid at every `x<=-1`, is

```text
s(t,x-1) = s(t+1,x) XOR (s(t,x) OR s(t,x+1)).
```

The boundary equality (1) holds through time `T+J-2`; the assumed
column-minus-one equality holds through `T+J-1`. Induction leftward
therefore gives period-`P` agreement at column `-j` for
`T<=t<=T+J-j`, for `1<=j<=J`. The first induction step uses the boundary
through `T+J-2`, and every further step shortens the available time
interval by one. In particular,

```text
s(T+P,-J)=s(T,-J).
```

Since all negative initial cells are zero and `c_0=1`, the leftmost one
at time `t` is exactly at `-t`. This follows by induction from
`f(0,0,1)=1` and `f(0,0,0)=0`, regardless of subsequent boundary values.
Thus `s(T+P,-J)=1`, whereas `-J<-T` implies `s(T,-J)=0`. Contradiction.

The same finite-interval proof works for Rule 90: left reconstruction and
the advancing edge suffice. It is a necessary finite-seed constraint,
not a Rule-30-specific exclusion.

## 4. Consequence for the zero-set obligation

Suppose, conditionally, that the actual lone-seed centre has period `P`
after `T_0`. For every `T>=T_0`, (1) holds. Also the true centre equation
and its period shift give

```text
l_(t+P) XOR l_t = (1-c_t) * (r_(t+P) XOR r_t),   t>=T_0.  (3)
```

Consequently every interval `[T,2T+P-1]` contains a time at which `c_t=0`
and `r_(t+P)!=r_t`. This is stronger than merely saying that the neighbour
cannot become `P`-periodic.

Take `T_(k+1)=2T_k+P`, starting at the onset. The intervals
`[T_k,T_(k+1)-1]` are disjoint, and

```text
T_k = 2^k (T_0+P) - P.
```

Each contains at least one zero-set mismatch. Thus their counting
function up to time `N` is at least `log_2 N - O(1)`; the constant may
depend on `T_0` and `P`. This applies to every positive multiple of an
eventual centre period.

An upper bound `o(log N)` for these mismatches at some period multiple
would therefore suffice for a contradiction. Such a bound permits
infinitely many mismatches, unlike eventual periodicity of the neighbour.
**No such upper bound is known here.** A useful theorem would have to
retain the zero-initial driven right history and the compatible left pin
or other seed information. This quantitative restatement is not asserted
to be logically easier than P1, and no generic periodic-drive estimate is
being assumed.

The [follow-up](RESULTS-r1-mismatch-followup.md) makes the missing glue
condition quantitative: for independently driven zero-initial halves,
`M_P(N)+2G(N+P)` has the same logarithmic lower bound, where `G` counts
centre-equation failures. The [exact Rule 90 control](RESULTS-r1-mismatch-sharpness.md)
shows logarithmic order and factor-two interval growth cannot be improved
by the rule-generic argument. Neither report supplies the missing upper
bound for compatible Rule 30 histories.

## 5. Verification and exact correction locations

```sh
uv run --no-project python \
  experiments/rule30/r1_periodic_realization_scope_audit.py
```

Besides the two tori and the two nonvacuous pin tests, the checker compares
direct scalar LHP evolution with an independent packed implementation on
all 2,048 length-twelve drives beginning in one. For each of Rule 30 and
Rule 90 it tests every `T>=0,P>=1,T+P<=6`: 43,008 drive/interval cases,
of which 7,680 meet the finite boundary hypothesis. Every eligible case
has the required mismatch. These are controls for the proof's indexing,
not evidence extrapolated to arbitrary periods or onsets.

The old-source corrections needed are narrowly located:

- Direct driven-LHP `PROOF.md`, lines 297–319: literal PIN-Pi is false by
  `110^infinity`; replace the purported open dichotomy with the
  nonconstant-tail version if that is the intended target.
- `RESULTS-r1-general-period.md`, lines 261–275: the two generic
  realizations exist in already recorded tori; withdraw the inference
  from their existence to a lone-seed period exclusion.
- The same general-period report's bounded `001`/`0001` zero-sample
  survival now has an exact infinite witness in the unrestricted
  initial-right-row domain. This does not upgrade other reported
  survivors or any zero-initial case.

No historical source, PATH row, or START-HERE entry is edited by this audit.
