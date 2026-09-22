# The Gamma observer is one extra B query

Date: 2026-09-14. **The apparent prefix recurrence in the inverse Gamma
map cancels exactly: its final value is the high output bit of one extra
B action.** This holds on every supplied input stream. On the actual
input B^(2k)(0), the low-bit query for (CA)^k(0) becomes a high-bit query
for B^(2k+1)(0) at the same digit index. Thus no additional prefix
observable is required to represent that query.

An optional aggregate implementation also folds the exact last-reset
summary over an existing repetition grammar. A three-state pullback
profile handles one K action without constructing its output digits.
The profile does not close under repeated actions, even on even inputs;
the exact four-digit witness below preserves all its boundary information.
The implementation retains and charges intermediate grammars when they
are needed. No uniform shrinking-index evaluation bound is proved.

The [verifier](../../experiments/rule30/p3_gamma_observer_grammar.py) and
[artifact](../../experiments/rule30/p3-gamma-observer-grammar.json) contain
the complete local factor table, the implementation, charged controls,
and the closure witness. No orbit census is used.

## 1. An exact two-state factor of the itinerary automaton

Write an input digit d=l+2h. In the
[itinerary ABC automaton](RESULTS-p3-itinerary-conjugacy.md), states A
and B have the same high-output rule, while C has the other rule:

| Entering state | Previous-high class a | High output |
|---|---:|---|
| A or B | 0 | h XOR l |
| C | 1 | 1 XOR h |

The following state is A or B precisely when the emitted high bit is0,
and C precisely when it is1. Consequently, for every input stream z,
the high bits of the K_B output obey

```
a_j = high(z_j) XOR (a_(j-1) OR low(z_j)),
a_(-1)=0.                                        (1)
```

The same recurrence with initial value1 gives the high bits of K_C(z).
K_A and K_B have identical entire high-bit output streams, because their
initial classes coincide. This is a literal factor of the transducer:
each of the12 state/digit cases preserves both its output and successor
class. No assumption about independence of the input digits is used.

Thus if F_W denotes the unary observer action of a finite input word W,
of nonzero length m,

```
F_W(0) = high((K_B(W))_(m-1)),
F_W(1) = high((K_C(W))_(m-1)).                     (2)
```

Finite-prefix transduction in (2) has its ordinary fixed initial state;
higher input digits cannot affect the result.

For the [inverse Gamma map](RESULTS-p3-itinerary-return-classes.md),
z=Gamma(y) is even and its inverse low-bit recurrence is exactly (1).
Therefore the complete inverse readout becomes

```
low(y_j)  = high((K_B(z))_j),
high(y_j) = low(z_(j+1)).                         (3)
```

Equation (1) holds for arbitrary z, including odd inputs; claiming (3)
as a Gamma inverse uses the even-input condition. On the actual orbit,
Gamma((CA)^k(0))=B^(2k)(0), so

```
low(digit_j((CA)^k(0))) = high(digit_j(B^(2k+1)(0))),
high(digit_j((CA)^k(0))) = low(digit_(j+1)(B^(2k)(0))). (4)
```

These hold for every k,j>=0. The inverse prefix recurrence can thus be
replaced by ordinary marked power queries. Appending a B node to a
generator expression is cheap; evaluating the resulting selected digit
still has its own cost. Equation (4) does not by itself reduce both the
power exponent and requested digit index.

The stronger [actual singleton reduction](RESULTS-p3-actual-b-query.md)
places both parities in the same marked family:

```
c_(2h+e) = bit_e(digit_(h-1)(B^(h+1+e)(0))),
h>=1, e in{0,1}.                                 (5)
```

Accordingly the aggregate construction below is an optional execution
method for a supplied expression, not a necessary additional scan in
the current representation of the singleton query. The verifier checks
the odd formula at n=1,3,17, including the n=1 boundary convention.

## 2. Exact last-reset metadata on a digit grammar

The [last-reset formula](RESULTS-p3-aggregate-affine-blocks.md) and its
four unary actions are already established. They are recalled here to
specify the new compiler, rather than claimed as a new monoid result.
For a digit word W store

```
S(W)=(length, last, parity),                      (6)
```

where last is the last index with low digit bit1, or None if there is
no reset. If a reset exists, parity is the XOR of high bits starting
at that last reset, including it. Otherwise parity is the XOR of all
high bits. Then F_W(a)=a XOR parity when last=None and
F_W(a)=1 XOR parity otherwise.

For W=UV, if V has a reset then

```
last(W)=length(U)+last(V), parity(W)=parity(V).
```

If V has no reset, retain last(U) and XOR the two parities. Lengths add.
For a repeat W^M, M>0, if W has a reset then

```
last(W^M)=(M-1)*length(W)+last(W),
parity(W^M)=parity(W).
```

Otherwise there is still no reset and parity is multiplied by M mod2.
The empty word has length0, no reset, and parity0.

These identities fold every concat/repeat node of the existing
[digit repetition grammar](RESULTS-p3-itinerary-repeat-transduction.md)
once. They return the exact reset position as well as the observer
action. No represented digit run is expanded. Each node uses a bounded
number of metadata operations; lengths, reset positions, repetition
counts, and their arithmetic remain charged. In particular an index
with b bits is not treated as a constant-size bit object.

## 3. A one-action pullback with all three boundary states

One can do more than summarize an already supplied output word. For a
digit word W and each possible entering K state g, store

```
R_W(g)=(p_W(g), S(K_g(W))),  g in{A,B,C},          (7)
```

where p_W(g) is the exact departing state. Let star denote the metadata
merge from section2. For a concatenation,

```
p_(UV)(g) = p_V(p_U(g)),
S(K_g(UV)) = S(K_g(U)) star S(K_(p_U(g))(V)).      (8)
```

This transports the actual intermediate state. Three records suffice
per digit-grammar node. For a Repeat node, follow the state orbit of
p_W from each initial g. The previously certified input-state monoid
has transient at most1 and cycle length at most2. Compose the prefix
metadata, apply the repetition formula to a full cycle, and compose its
remaining suffix. At most three child-state records are visited for
each entering state, independently of the represented repeat count.

Induction on grammar nodes proves that (7)-(8) compute one K action's
observer summary without constructing its output word or output grammar.
The integer arithmetic in the repeat calculation is charged separately.

This avoids the 2^m lower-prefix contexts of the
[full section-reward table](RESULTS-p3-section-reward-action.md) when a
small digit grammar is already available. It is not a uniform complexity
comparison between the two algorithms: the earlier table starts with
a generator expression, whereas (7) needs a digit grammar for the
actual input. Obtaining and maintaining that grammar can dominate the
cost. The two statements cannot be combined by assuming that conversion
is free.

## 4. Paid evaluation from an existing generator expression

The executable evaluator accepts the existing QuaternarySLP format for
generator powers or sections, and the existing RepeatSLP format for
input digits. For an internal generator expression UV it first applies
U to the actual input grammar, then applies V to the resulting grammar.
Applications are memoized by both generator-node identity and input
grammar-node identity. Repeated occurrences of one generator expression
with different input grammars are distinct paid contexts.

When only the final observer is required, the evaluator applies all
preceding generator children and uses (7) for the final generator leaf.
It therefore need not construct the last output grammar. It records
generator grammar construction, intermediate digit grammar construction,
transduction contexts, observer-profile nodes, metadata operations, and
the maximum metadata bit width.

This is exact for every supplied finite generator expression and digit
grammar. It is not an autonomous powering law on the summaries. A
logarithmic-size expression for B^N can still cause many distinct
generator/input contexts or large intermediate grammars. No bound
sublinear in N is asserted.

As a directed compressed-input control, the program evaluates the
observer on B squared applied to0^M, where M=2^40+7. Here the actual
output is2^M, and (1) toggles at every digit, so the answer is1. The
implementation constructs seven digit-grammar nodes, uses two digit
transduction contexts and two three-state profile nodes, and records
41-bit metadata. It does not expand M digits. The generator exponent is
the fixed value2; this control is not a growing-index singleton speedup.

## 5. The profile cannot replace the intermediate output grammar

Even augment (7) by the raw input summary S(W), so the profile retains
the input's length, exact last reset and suffix parity, plus all three
departing states and all three corresponding output summaries. The
following even input words have exactly the same augmented profile:

```
X=0010, Y=0110,                                  (9)
```

read low digit first. Both raw summaries are(4,2,0). For every entering
state A,B,C, both words depart in state C and have output summary
(4,3,1). Nevertheless their next two B actions give

| Input | B(input) | B squared(input) | Final summary | Observer from0 |
|---|---|---|---|---:|
| 0010 | 1123 | 2210 | (4,2,0) | 1 |
| 0110 | 1223 | 2130 | (4,2,1) | 0 |

Thus there is no deterministic update of this augmented profile under
one B action that remains sufficient for the next observer. Otherwise
equal initial profiles would remain equal through two updates and
would predict equal answers. The witness retains the exact ordered
state transport and even-input guard; it does not arise from replacing
the three boundary states by independent marginals.

These are arbitrary even auxiliary inputs. They are not asserted to be
B^(2k)(0) prefixes, and no actual-seed ancestry is inferred from their
origin digit. This refutes the specified all-input profile closure, not
a quotient proved only for the actual orbit or every possible summary.

## 6. Verification scope

The saved checker includes12 complete local cases of the high-output
factor,32 two-digit factor controls,20 grammar/repeat controls covering
all three entering states, and the exact even-input closure witness.
It checks12 actual CA readouts against the already saved return-class
artifact, using both the optional aggregate and the appended-B query.
Three small odd singleton checks use the independent center engine.
The fixed huge-repeat control records all grammar and metadata costs.

The all-length results follow from the local factor, exact state
transport, grammar induction, and invariant even-input readout. The
controls verify their implementations. They do not establish a bound
on intermediate grammar growth or an efficient bulk power construction.
