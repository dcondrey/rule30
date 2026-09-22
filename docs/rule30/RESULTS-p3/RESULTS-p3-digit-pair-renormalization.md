# Exact obstructions to the first digit-pair renormalizations

Date: 2026-09-13. **The simplest index-halving codes for the itinerary
automaton fail by exact root and seam constraints.** Every injective
uniform digit-to-pair embedding fails within two source digits. A total
decoder on all inputs cannot intertwine the two dynamics even without
causality or memory restrictions. A decoder restricted to the actual seed orbit remains
open; the first four exact orbit rays already show that it needs memory.

The [verifier](../../experiments/rule30/p3_digit_pair_renormalization.py)
and [artifact](../../experiments/rule30/p3-digit-pair-renormalization.json)
use the complete16-value root table, eight surviving injective codebooks,
and finite phase-state certificates for six infinite-ray actions. They perform
no center-prefix regeneration or growing compression census.

## 1. Definitions and the exact first-pair map

Use K=K_C from the
[itinerary conjugacy](RESULTS-p3-itinerary-conjugacy.md). Its initial
digit permutation is d->3-d. The initial state is reset to C whenever a
new K action is applied. Digits are low first. A pair (a,b) is represented
by its decimal integer a+4b; these integers are not single base-four digits.

Let T be the action of K squared on the first two digits. Directly from
the three-state automaton,

| v | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| T(v) | 4 | 1 | 10 | 15 | 8 | 13 | 6 | 3 | 12 | 9 | 2 | 7 | 0 | 5 | 14 | 11 |

Thus its fixed points are1,6,9,14, its two-cycles are(2,10) and(5,13),
and its remaining points lie in two four-cycles. The verifier separately
obtains this entire table from Phi(C squared(Phi inverse(v))), retaining
two itinerary digits. No assumption about independent digit states is used.

In this report function products have their usual mathematical order:
K squared E means apply E first, then K twice. Generator words inside the
verifier retain the repository's chronological convention.

## 2. No injective uniform pair embedding

Suppose E replaces each source digit d by a fixed pair f(d), with four
distinct code pairs, and satisfies

```
K^2(E(x)) = E(K(x))  for every input x.            (1)
```

Comparing just the first pair forces

```
T(f(d)) = f(3-d).                                 (2)
```

Injectivity means each complementary source pair must occupy a distinct
two-cycle of T. Therefore the image is exactly{2,10,5,13}. Choosing the
cycle and orientation for f(0), and the orientation of the other cycle
for f(1), leaves precisely eight codebooks. There is no unexamined
injective letter-pair code outside this list.

All eight fail at the next input digit. The table gives one two-digit
source prefix witnessing each failure. Source prefixes are written low
first; codebook entries remain decimal pair encodings.

| (f(0),f(1),f(2),f(3)) | Source prefix |
|---|---|
| (2,5,13,10) | 00 |
| (2,13,5,10) | 00 |
| (10,5,13,2) | 00 |
| (10,13,5,2) | 00 |
| (5,2,10,13) | 11 |
| (5,10,2,13) | 10 |
| (13,2,10,5) | 00 |
| (13,10,2,5) | 00 |

The exact comparison retains a pair of states: the two-letter section
word of the fine K squared action and the current state of the coarse
K action. On input d, it compares the fine output from the actual pair
f(d) with f applied to the actual coarse output, and then advances both
states. There are at most27 such state pairs. The artifact records each
failing state, both unequal output pairs, and the unequal complete
four-digit output prefixes. Any continuation of a displayed input prefix
remains a counterexample by causality. This is an exhaustive refutation
of (1) in the stated uniform injective code family, not a finite guess
about a larger encoder class.

## 3. The zero seed rules out a broader causal embedding

There is a separate obstruction to seed-preserving embeddings that need
not be uniform or injective. Suppose the first two digits of E(x) depend
only on x's first digit, with a fixed initial encoder state. Assume (1)
and E(0)=0, where0 means the entire zero ray. Iterating (1) twice gives

```
K^4(0) = E(K^2(0)).                               (3)
```

K squared fixes the first source digit0. Therefore E(K squared(0)) must
have the same first pair as E(0), namely00. But T squared(0)=8, whose
pair is02. This contradicts (3).

This includes stateful digit-to-pair encoders that emit their first pair
after reading just the first digit. It does not include an encoder whose
first pair reads a larger source prefix, an altered boundary or seed,
or a decoder in the reverse direction. In particular a fixed finite
state count alone is not the hypothesis of this theorem: the precise
first-output dependence is essential.

## 4. No total intertwining decoder, with or without causality

There is a stronger obstruction than the first-pair one below. The
exact infinite rays satisfy

```
K((12)^infinity) = (21)^infinity,
K((21)^infinity) = (12)^infinity.                  (4a)
```

The two state-and-input-phase orbits close after respectively three and
two checked transitions, starting in C. Thus K squared has a fixed point
x=(12)^infinity.
K has no fixed point at all, since its first digit is always complemented.
If any total map D satisfied D(K squared(x))=K(D(x)), its value D(x)
would have to be a fixed point of K. This is impossible. No causality,
finite-state, continuity, or lookahead assumption is needed. This
strengthening was found during the independent certificate audit and
its two exact phase cycles are preserved in the verifier.

For completeness, the original first-pair obstruction gives a separate
local proof for the proposed two-to-one implementation:

Suppose a fixed-initial-state decoder D emits its first output digit
after reading its first pair, and is defined on every input ray. Write
f(v) for that first output digit; internal state after the pair can be
arbitrary. An all-input identity

```
D(K^2(x)) = K(D(x))                               (4)
```

would imply f(T(v))=3-f(v) for every pair v. At any fixed point of T,
this requires a base-four digit to equal its complement. None does.
Thus (4) is impossible, regardless of the decoder's subsequent memory.

These obstructions do not apply when (4) is required only on the actual
seed orbit, which is the restricted question considered here. Extending
a proposed decoder to arbitrary inputs would therefore discard a
potentially decisive restriction. The exact criterion for that restricted
causal problem is recorded in
[actual-orbit decoder causality](RESULTS-p3-actual-orbit-decoder-causality.md).

## 5. What survives on the actual orbit

The first four exact K iterates of the zero ray are

```
K^0(0) = 0^infinity,
K^1(0) = 3^infinity,
K^2(0) = (01)^infinity,
K^3(0) = (32)^infinity,
K^4(0) = (02)^infinity.                           (5)
```

Each equality follows from the finite state-and-input-phase orbit of
one transduction, with initial state C. The verifier closes those orbits
exactly; it does not infer infinite periodicity from a long matching
prefix.

A stateless decoder on consecutive nonoverlapping pairs cannot satisfy

```
D(K^(2L)(0)) = K^L(0)  for all L>=0.              (6)
```

At L=2 every input pair in K fourth(0) is02, so its decoded output would
be constant, whereas the required K squared(0) is the alternating01
ray. A stateful decoder can at least distinguish the two phases, so this
does not refute it. It proves only that any successful decoder in this
model must use at least two reachable internal states on the constant
02 block stream. No finite-state decoder satisfying (6) is established
here, and even such a decoder would still need an evaluation-cost and
query-index argument before giving a P3 speedup.
