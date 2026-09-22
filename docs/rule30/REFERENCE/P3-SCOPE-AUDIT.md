# Scope audit of Rule 30 Prize Problem 3

Date: 2026-09-03

## Verdict

**The official prose and displayed asymptotic predicate are not equivalent.**
This does not solve P3 and should not be exploited as a semantic prize claim.
It does mean that a proposed lower-bound proof must state its predicate
explicitly and obtain clarification before submission.

Primary source: Stephen Wolfram,
[*Announcing the Rule 30 Prizes*](https://writings.stephenwolfram.com/2019/10/announcing-the-rule-30-prizes/),
2019.  The current [prize site](https://rule30prize.org/) links the same three
questions.

## 1. Three different asymptotic statements

Let `T_M(n)` be the number of steps taken by a fixed Turing machine `M` on the
digit representation of `n`.  At least three natural predicates occur around
the announcement:

```text
(A) every correct M has T_M(n) = Omega(n),
(B) no correct M has T_M(n) = o(n),
(C) no correct M has T_M(n) = O(n).
```

The headline wording, “require at least O(n),” conventionally intends `(A)`
after replacing `O` by `Omega`.  The surrounding narrative asks about
algorithms taking much less than `n` steps and gives logarithmic behavior as a
model, which points toward `(B)`.

The displayed formal predicate instead negates the existence of a correct
machine whose `limsup T_M(n)/n` is finite.  That is `(C)`, modulo the usual
minor distinction between a finite limsup and an eventual big-O bound.  It
would reject a correct `Theta(n)` algorithm, even though such an algorithm
satisfies “requires at least linear effort” and is not sublinear.

For irregular time functions `(A)`, `(B)`, and `(C)` are not interchangeable:

- `T(n)=n` satisfies `(A)` and violates `(C)`;
- a time bound alternating between `1` and `n^2` is neither `Omega(n)` nor
  `O(n)`, and is not `o(n)`;
- `T(n)=sqrt(n)` is `o(n)` and violates both intended linear lower-bound
  readings.

Thus the mismatch is mathematical, not merely a choice of notation.

## 2. Operational convention for this repository

Until the organizers clarify the predicate, this repository uses the
narrative falsification target:

```text
exhibit one uniform correct machine with T(n)=o(n).
```

That is the conservative meaning used by the binary-kernel, observational
quotient, support-set, and Hashlife probes.  A measured exponent below two but
above one is only a speedup over naive spacetime simulation; it is not a P3
answer.  A `Theta(n)` construction would be important and would contradict
the displayed formal predicate, but it would not be reported as a prize
solution without a ruling from the organizers.

For a positive lower-bound result, the manuscript must choose one of `(A)` or
`(B)` and prove it in the stated Turing-machine model.  Neither arbitrary-row
decision-tree depth nor the size of one derivation system establishes either
predicate for the fixed sequence `n -> c_n`.

## 3. A second model detail to make explicit

The announcement treats numeric `n` as the asymptotic variable even though
the input has only `Theta(log n)` digits.  This asks for an exponential lower
bound in ordinary input length.  A rigorous submission should therefore
specify:

1. the tape model and alphabet;
2. whether `T_M(n)` is the pointwise runtime on integer `n` or a worst case
   over all inputs of the same bit length;
3. the treatment of malformed encodings and leading zeros; and
4. whether the desired conclusion is an eventual lower bound, a liminf
   bound, or only exclusion of a limiting sublinear ratio.

The existing P3 work in this repository uses pointwise canonical binary
encodings because that is closest to the announcement.  This scope choice
must accompany every claimed asymptotic result.


## 4. Session integration: exact operators do not erase construction cost

Updated 2026-09-14. The working model is one deterministic uniform
finite-alphabet multitape Turing machine, canonical binary n (zero encoded
as `0`), read-only input, initially blank work tapes, one exact output bit
and no growing advice. Charge preprocessing, construction, decoding,
arithmetic, memory access and total sequential work. A RAM or parallel
claim needs a cost-preserving translation before use in this model.

The [current itinerary investigation](RESULTS-p3-implicit-boundary-investigation.md)
proves exact singleton correspondences and guarded observers. Its finite-core
powering and supplied-repeat transduction are valid shortcuts on their stated
inputs. They are not dismissed for being restricted, but the required actual
input objects have not been constructed with sublinear charged work.
The newest next step is that constructor, retaining complete ordered controls
and both B/C origin terms. Source-reviewed all-input arguments and bounded
checker replays are labeled separately; no P3 Lean theorem is claimed.

Neither exclusion of a fixed representation nor a bound on explicit local
evaluation proves `(B)`. An eventual Omega(n) theorem `(A)` is stronger than
the operational exclusion of o(n); this update does not resolve either or
refresh the historical official-wording review as if a new external ruling
had been obtained.
