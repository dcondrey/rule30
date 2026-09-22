# Automaticity routes: stale obligations and an overbroad rejection

Date: 2026-09-15. **No Rule 30 problem is solved.** This audit integrates an
existing generic counterexample, corrects one exact state count, and narrows
an invalid rejection of a conditional proof strategy. No larger Rule 30
prefix or circuit search was run.

## 1. Lemma L was already refuted

The original [automaticity report](overnight/RESULTS-automaticity.md),
lines 95–107, and [PATH row 46](PATH.md), line 675 at audit time, still
advertise the generic implication

```text
k-state automatic => Ore order poly(log k), height poly(k).
```

Both bounds were already refuted in
[the a20 source audit](../../experiments/overnight-arms/frontier_attack/a20_bridy_verification/bridy_verification.md),
sections 4–5. PATH section 9.3, row 46 (line 1342 at audit time), already
records the later outcome. The outstanding work is index integration, not
proving Lemma L or repeating the proposed generic finite search.

In particular the existing Artin–Schreier family
`G_r=sum_(j>=0) x^(2^(r*j))` has exactly `r+2` kernel states and minimal
inhomogeneous Ore order `r`. This refutes a bound polynomial in `log k`.
These are auxiliary automatic sequences, not Rule 30 center sequences.
The established Rule 30 finite rank certificates and the equivalences
`S(0) <=> P1` and `all S(r) <=> nonautomaticity` remain unaffected.

## 2. Correct the monomial witness's exact state count

The a20 report, lines 194–207, turns its quoted monomial example into the
claim that `x^(2^(k-1))` has exactly `k` states. This is incorrect under
the report's stated convention: state count is the cardinality of the
full binary kernel. For `r>=0` the exact kernel of `x^(2^r)` is

```text
{x^(2^r), x^(2^(r-1)), ..., x, 1, 0},
```

so its cardinality is **`r+3`**. Here `1` denotes the sequence supported
only at index zero, and `0` denotes the all-zero sequence. The two Cartier
operators send `x^j` to `x^floor(j/2)` in the matching parity and to zero
in the other parity. Repeated zero sections reach `x`; its one section
reaches `1`; a mismatched section reaches zero. This proves closure,
reachability, and distinctness of every listed state.

The minimal Ore height of `x^N`, `N>=1`, is still exactly `N` in the
original report's inhomogeneous convention. If coefficient degrees are
less than `N`, the supports of the constant polynomial term and the
terms `P_i(x)x^(N*2^i)` lie in disjoint intervals, so no nonzero relation
can cancel. The relation `x^N+F=0` attains height `N`. Thus a correct
exact witness is **height `2^(k-3)` with `k` states, for every `k>=3`**.
Exponential height remains necessary; the generic rejection stands.

The primary [Bridy paper](https://arxiv.org/pdf/1604.08241), Example 2.14,
prints the state-count expression copied by a20, while its preceding
kernel characterization identifies the count with kernel cardinality.
This audit corrects the exact mathematical count, not the fidelity of
a20's quotation. Proposition 2.13 and the separate data-cost table are
not changed by this correction.

An independent standard-library Cartier-closure check, run with
`uv run --offline --no-project python`, verified all monomial exponents
`1..4096` and the powers `2^r` for `0<=r<=16`. It found
`|K_2(x^N)|=bit_length(N)+2`; for example `x^8` has six states.
The proof above is all-length; those finite checks are controls.

## 3. The subsequent conditional-proof rejection is too strong

The [a22 follow-up](../../experiments/overnight-arms/frontier_attack/a22_row46_specific_uniformity/specific_uniformity.md),
lines 59–75, calls a state-count-independent bound “definitionally
unavailable” and calls assuming automaticity circular because automaticity
is allegedly P1's negation. Both assertions need correction.

P1 asserts non-eventual-periodicity. Its negation is eventual periodicity,
which implies automaticity. The converse fails: Thue–Morse is automatic
and not eventually periodic. Nonautomaticity is therefore sufficient for
P1, and is a stronger target.

Assuming automaticity in a contradiction argument is legitimate. For
example, either of the following would suffice for nonautomaticity:

```text
Automatic(c) => some Ore relation of order <= r0,
together with the all-height statement S(r0);

Automatic(c) => some Ore relation of order <= r0 and height <= d0,
together with the finite certificate S(r0,d0).
```

The constants must come from an independently proved Rule-30-specific
argument. A finite certificate `S(r0,d0)` alone does not prove `S(r0)`.
Likewise, a bound growing without limit with unknown state count does not
turn one finite certificate into an exclusion of all automatic models.
These valid limitations support “no such conditional bound obtained,”
not a logical impossibility theorem for conditional bounds.

## 4. The latest exact identities do not supply that bound

The [actual B query](RESULTS-p3-actual-b-query.md) gives an exact formula
for both binary decimations of the center sequence. However, its requested
power exponent and digit index both grow with the input. The three-state
spatial transducer is not a finite-state machine reading the binary time
index.

The [two-channel block construction](RESULTS-p3-b-two-channel-block.md)
does halve time and spatial index once, retaining both coupled fields.
It proves no fixed family closed under arbitrarily many such halvings.
The [causal-decoder report](RESULTS-p3-actual-orbit-decoder-causality.md),
section 2, explicitly distinguishes even decoder existence from finite
state, efficient construction, and reconstruction in the direction needed
by a fast query. These results presently provide neither a uniform Ore
order/height bound nor an automaticity contradiction. No new direct
query upper bound follows from this audit.

## 5. Row 93 has a separate scope correction

The [bounded circuit report](RESULTS-bounded-circuit-synthesis.md),
lines 349–351, says its width-dependent functions are not refinements and
their complexities are not comparable. In fact they satisfy the exact
restriction identity

```text
f_(m+1)(0,b_(m-1),...,b_0)=f_m(b_(m-1),...,b_0).
```

Their circuit-complexity sequence is a meaningful object. What is missing
for P3 is a uniform, costed construction and evaluation of the circuits;
independent finite synthesis does not establish such a construction.
The small exact lower bounds and the reported solver limits stand. This
correction does not justify a larger synthesis run without a new encoding
or a proposed cross-width construction law.
