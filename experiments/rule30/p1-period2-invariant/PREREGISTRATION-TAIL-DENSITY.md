# Preregistration: hard-core reconstructed-tail density

Date: 2026-09-01

## Candidate uniform lemma

Let `rho_0,...,rho_(n-1)` contain no adjacent ones.  Feed the exact rotated
Rule 30 reconstruction with

```text
v_(2k)   = 1-rho_k,
v_(2k+1) = 1,
```

and let `L_1,...,L_(2n)` be the emitted initial left-tail bits.  Prove

```text
7 * sum_(j=1)^(2n) L_j >= 2n-2.                    (D)
```

Any eventually-zero reconstructed tail has bounded prefix weight, whereas
the right side of (D) diverges.  Therefore (D), combined with the exact
bilateral no-`11` reduction, would prove the period-two same-orbit theorem.
It would still not prove arbitrary-period P1.

The coefficient seven is fixed before the proof search.  It is suggested by
the exact period-seven infinite-left control: the alternating hard-core word
`rho=0101...` reconstructs the periodic tail `1000000...` in the registered
alignment.  Thus a positive-density theorem must allow this control rather
than falsely exclude it.

## Candidate proof language

Seek a discharging identity for the full triangular reconstruction, not a
strict rank on forced post-knee macros.  The primary form is

```text
7 * (new emitted ones) - 2
  + Phi(next boundary state) - Phi(current boundary state) >= 0,
```

summed over seed macros.  `Phi` may use:

- the hard-core automaton state;
- time modulo 7;
- the exact four-carry/D8 action;
- a finite defect mode relative to the period-7 extremal wallpaper; and
- a nonnegative unbounded defect count with a separately proved local update.

The terminal bound on `Phi` must be uniform, so storing the raw frontier or
an endpoint window whose size grows with `n` is not permitted.  A two-
dimensional local tile/discharging proof is also admissible if every interior
term cancels and only the displayed boundary weights remain.

## Fixed falsification and synthesis experiment

1. Independently reconstruct every hard-core word through `n=24`; record the
   exact minimum tail weight, minimum slack in (D), and all equality cases.
2. Verify symbolically that `rho=0101...` gives a period-seven reconstructed
   tail, including the boundary alignment.
3. Build the transition graph of seed-prefix extensions for summaries
   `(n mod 7, previous rho, D8 action)` and the registered defect refinements.
   Solve the exact difference constraints for `Phi` by Bellman-Ford/Farkas;
   independently verify any integer potential on the complete finite edge
   alphabet.
4. If a finite potential survives, derive its transition table for arbitrary
   frontier words with the carry transducer and prove the induction
   symbolically.  Sampled feasibility is not success.

Limits: `n<=24`, defect radius at most four, at most 128 finite observer
modes, ten minutes, 2 GiB.  Do not increase these after a negative cycle.

## Success criterion

Success requires a human-readable all-`n` proof of (D), an independent finite
table checker for its local cases, and an explicit final deduction from
eventually-zero `L` plus no-`11` rho to the period-two theorem.

## Kill conditions

- Any hard-core prefix through `n=24` violates (D).
- The period-seven control does not reproduce in the exact reconstruction.
- The primary observer or any registered refinement has an exact reachable
  negative cycle; do not enlarge the observer after that cycle.
- A candidate needs a frontier-sized potential, has unbounded negative
  terminal value, or silently assumes a bounded zero gap (known long survivor
  suffixes have arbitrarily growing candidate gaps).
- The derivation transfers unchanged to Rule 90 or excludes the infinite-left
  period-seven control.
- Independent integer, symbolic ANF, SAT, adversarial Rule 30, or Rule 90
  controls disagree.

A failure kills only the registered coefficient-seven discharging language,
not other global tail-density inequalities or mortality itself.

## Controls

- Minimum weights through `n=24` must reproduce
  `1,1,1,2,2,2,2,2,3,3,4,4,4,4,5,5,5,6,6,6,6,7,7,7`.
- The length-22 mortality witness must retain its recorded 12-macro zero
  suffix; no fixed-gap lemma may be inferred.
- Rule 30 `{-8,-1,6}` alternates through time 14 and fails at 15.
- Rule 90 `{-1,1}` has zero center forever (checked through time 128).
