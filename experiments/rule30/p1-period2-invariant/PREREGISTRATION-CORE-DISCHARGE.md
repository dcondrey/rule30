# Preregistration: active-core discharging and grammar

Date: 2026-09-01

## Target

Prove a seed-dependent mortality bound for the exact active-core map

```text
v -> G(v) = Transduce(v) . 3
```

where the four-state carry starts at zero, every accepted word has final
carry bits unequal, and successive forced rho bits avoid `11`.  It is enough
to prove mortality for all finite cores; a theorem restricted to the exact
seed-generated sublanguage is also acceptable if that restriction is proved
uniformly.

## Certificate classes to test

1. A local two-dimensional discharging rule on the exact Mealy spacetime,
   with a telescoping boundary term and a strictly positive charge over any
   sufficiently long accepted orbit.
2. A finite grammar of word intervals carrying symbolic endpoint states,
   closed under `G`, together with a well-founded multiset or stack order.
3. A recursive block identity for arbitrary words, checked by exhaustive
   enumeration only over the finite carry/interface alphabet; word length
   must remain universally quantified.

A finite automaton accepting all tested cores, a bounded-width UNSAT table,
or a potential verified only through a maximum length is not a certificate.

## Search limits and controls

- Exhaustive exploratory cores: length at most 20 unless a smaller exact
  counterexample already kills the class.
- Local discharging radius: at most 4 in the time direction and 5 in the word
  direction before reassessing the ansatz.
- Any proposed local identity must be verified on every assignment in its
  finite support and then derived algebraically from the carry table.
- Any grammar must ship an independent closure checker that reasons over its
  finite productions, not enumerate full words.
- Mandatory positive controls: the finite Rule 30 row supported on
  `[-164,13]` recorded in `RESULTS-JOINT-MORTALITY.md` must not be rejected
  before time 185.
- Mandatory negative controls: the infinite-left period-seven wallpaper must
  remain outside the finite-core hypothesis, and the argument must use the
  Rule 30 OR operation in a way that fails for the Rule 90 `{-1,1}` control.

## Kill conditions

- An exact accepted cycle with nonpositive total charge kills the associated
  finite local discharging observer.
- Two words with the same proposed grammar annotation but incompatible
  successors kill deterministic closure at that annotation.
- A core surviving beyond the proposed seed-dependent bound kills that bound,
  but not period-two mortality.
- If every bounded annotation merely refines the already-killed D8 observer,
  stop rather than increasing its radius.

## Reporting rule

State separately whether the outcome is a uniform proof, a uniform
intermediate lemma, or only a finite/negative result.  No finite experiment
may be described as proof of period-two mortality.
