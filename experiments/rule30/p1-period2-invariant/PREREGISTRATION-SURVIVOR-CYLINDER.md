# Preregistration: survivor-cylinder ideal grammar

Date: 2026-09-01

## Theorem target

Prove uniformly that the Boolean survivor variety

```text
V_(2n+2) = empty
```

for every hard-core seed length `n`.  This is exactly linear hard-core
mortality.  Combined with the recorded bilateral reduction it would prove the
period-two same-orbit theorem, but not arbitrary-period P1.

## Candidate certificate

The `n=10` Bezout certificate shows a delayed contradiction: `epsilon_8` is
already one on `V_3`, although it is not queried until macro eight.  Its
plateau variety is a small cylinder-like set of seeds.  Test whether every
nonempty survivor variety admits a canonical decomposition into

```text
forgotten shallow prefix  x  bounded moving core  x  forced deep suffix,
```

where the core is represented by an ordered list of marked seed positions,
not by a fixed collection of parities or moments.

The desired grammar has finitely many symbolic rewrite *schemata* whose
indices are affine functions of `n` and the current macro offset.  A rewrite
may shift or delete an arbitrary forgotten prefix in one step, but it must
retain every marked position and give an exact Boolean ideal basis for the
survivor cylinder.  Each nonterminal schema must either:

1. advance the macro offset while decreasing a nonnegative affine credit; or
2. expose a future pin/no-`11` generator that reduces to one modulo the current
   cylinder ideal at an offset at most `2n+1`.

This is not a bounded frontier summary: the ordered marker list may grow with
`n`.  Success requires a well-founded statement about that full list and an
induction checking every symbolic rule.

## Fixed experiment

1. Enumerate exact survivor sets for every `n=1,...,24` and every horizon
   through first death, using the canonical integer recurrence already
   validated against SAT.
2. For each set compute:
   - equivalence classes by exact `seed_state` and by every later exact
     frontier state;
   - the lexicographically canonical Boolean cylinder basis obtained by
     Shannon splitting in chronological seed order;
   - forced-zero, forced-one, free, and dependency positions;
   - for every future failure polynomial, its earliest survivor variety on
     which it is identically one.
3. Normalize positions relative to both seed endpoints and search for exact
   repeated rewrite schemata across consecutive `n`.  Use no SAT proof traces
   and do not extend the seed bound beyond 24.
4. Any proposed schema must be checked independently by expanding its Boolean
   basis to the full seed set through `n=18`, then proved symbolically for all
   indices.  Total search budget: ten minutes and 2 GiB.

## Success criterion

Finite repetition is not success.  Promote only an explicit finite list of
index-parameterized ideal rewrites, a well-founded credit proving a terminal
offset below `2n+2`, and a separate checker for every finite side condition.

## Kill conditions

Stop and record a negative for this certificate class if:

- two survivor sets with the same normalized cylinder basis require
  incompatible next rewrites;
- exact state equivalence does not account for the apparent free prefix;
- the number of dependency markers or distinct normalized rules grows at
  every tested `n` without an exact recursive constructor;
- a basis needs non-cylinder polynomial relations whose support spans a
  growing fraction of the seed and no shift recurrence closes them;
- a proposed credit also proves mortality for the infinite-left period-seven
  wallpaper or for Rule 90;
- any survivor, ANF, SAT, Rule 30 adversarial, or Rule 90 control disagrees.

A negative kills only the finite-schema cylinder decomposition.  It does not
kill dynamic Boolean ideals, unbounded grammars, mortality, or the alternative
eventual-periodicity route.

## Controls

- Reproduce the registered maximum survival sequence through `n=24`.
- Recheck every survivor set by direct replay and all `n<=12` counts against
  `ideal-variety-n4-n12.json`.
- Preserve the length-4 seed `0xa` survival-four endpoint-peel obstruction.
- Rule 30 `{-8,-1,6}` first fails the alternating trace at time 15.
- Rule 90 `{-1,1}` keeps zero center through time 128.
