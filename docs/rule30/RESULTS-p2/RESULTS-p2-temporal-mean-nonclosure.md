# P2: the four-step temporal-mean nonclosure

Date: 2026-09-09. **P2 is not solved; no ladder rung is reached.**

This attempt used the sharpened energy criterion and the exact identity
`H(z)=N+4H(A)` to seek an evolution on temporal averages that could be
iterated across scales. The first step works as an exact representation:
the two-step average of a whole Rule 30 spatial row has a local inverse.
The next averaging step fails to close, on two explicit period-14 rows.
Their four-step averages agree at every spatial position, but their
eight-step averages at column zero are +1/4 and -1/4.

This is a uniform obstruction to an evolution or scale-doubling rule that
uses only the averaged row. It is not a counterexample to lone-seed P2,
and it does not exclude inequalities using additional seed information.

Follow-up: [the ordered-energy audit](RESULTS-p2-ordered-energy-audit.md)
tests an inequality retaining temporal order. It gives a sufficient
accumulated-loss criterion, but no seed-specific estimate of that loss.

## 1. Exact object and tested mechanism

For a binary configuration x, write F for Rule 30 and define the spatial
field of temporal averages

```
Phi_T(x)_i = (1/T) sum_(t=0)^(T-1) [1-2(F^t x)_i].
```

Each coordinate is averaged in **time**, not across space or across
initial configurations. The first pair field in the preceding report is
`Phi_2(F^(2n) delta_0)_0`. At the actual seed row at time N, higher
temporal blocks appearing in H have this form with T a power of two.

The proposed mechanism was to find an exact evolution `K_T` with

```
Phi_T(F^T x) = K_T(Phi_T(x)),
```

and then use

```
Phi_(2T)(x) = [Phi_T(x)+Phi_T(F^T x)]/2
```

to obtain a strict energy bound. The diagnostic failure condition was
two configurations with the same complete input mean field and different
next or doubled mean fields. That condition fires at T=4. The evidence
does not establish or assume a contraction at any scale.

| Statement | Evidence | Domain |
|---|---|---|
| Local inverse of Phi_2 | U/C | Every Rule 30 configuration; deterministic, not a.e. |
| Radius-four evolution on Phi_2's image | U/C | Every Rule 30 configuration; complete finite local check |
| Phi_4 does not determine Phi_8 or the next four-step mean | U/C/K | Explicit periodic configurations; **not lone seed** |
| No fixed-radius mean-only rule even on all finite-support rows | U/K | Every proposed fixed radius; arbitrary finite-support rows, not the designated seed |
| Temporal means retain right-asymptotic rows injectively | U | Left-permutive rules including Rules 30 and 90; not a density statement |
| A seed-specific estimate H_k=o(2^(2k)) | **Unproved** | The actual lone-seed orbit only |

## 2. The two-step mean retains the entire row (U/C)

Put `a_i=Phi_2(x)_i`. Since

```
a_i = 1-x_i-[x_(i-1) XOR (x_i OR x_(i+1))],
```

each a_i belongs to {-1,0,1}. There is an explicit decoder

```
x_i = D(a_i,a_(i+1),a_(i+2)),

D(p,q,r)=1 iff
    p=-1,
    or p=0 and q=0 and r!=-1,
    or p=0 and q=1 and r=-1.
```

Otherwise D=0. This formula is needed only on triples that actually occur
in a mean field.

**Proof.** Values a_i=1 and -1 directly determine x_i=0 and 1.
When a_i=0 and x_i=0, the original triple is either 001 or 100.
The former gives a_(i+1)=-1. In the latter, the following bit gives
either `(a_(i+1),a_(i+2))=(0,-1)` or `(1,r)` with r in {0,1}.
All these cases decode to zero.

When a_i=0 and x_i=1, the left bit is one. If the right bit is zero,
the next bit gives either `(0,r)` with r in {0,1}, or `(1,-1)`.
If the right bit is one, the next mean is zero and the following mean
cannot be -1. These cases decode to one. They exhaust the rule table.

Equivalently, every relevant expression depends on precisely five input
bits, so checking all 32 five-bit words is a complete finite proof.
There are 16 admissible mean triples; the exact decoder table is saved
in the certificate. No infinite-length extrapolation is involved.

Two consecutive mean entries alone do not suffice: input words `1000`
and `1101` both give `(a_i,a_(i+1))=(0,1)` but have different x_i.

Consequently Phi_2 is injective on the entire binary full shift and has
a local inverse. Pair averaging has not reduced the information in the
whole spatial state. This strengthens the previous report's observation
that the averaged field has a different alphabet: it can in fact evolve
autonomously, by conjugating F^2 through this decoder.

The direct decoder composition gives a finite neighborhood bound. A
complete smaller local calculation proves that the next pair mean is
determined by mean entries at positions i-4,...,i+4. All 2,048 binary
input windows of length 11 yield 1,024 mean windows of length 9, each
with a unique next pair mean. Radius three fails: the input windows

```
000011001
000011100
```

give the same seven mean entries `(1,1,0,-1,0,0,0)`, while the next
pair mean at the central site is respectively 0 and 1. Thus symmetric
radius four is sufficient and minimal for this particular evolution.
This is a local representation theorem, not an energy contraction.

For the lone seed, the initial mean field is all ones except
`(a_-1,a_0,a_1)=(0,-1,0)`. Its exact evolution under this representation
is established; its long-time central average remains unbounded by the
present argument.

## 3. Four-step means lose information needed at the next scale (U/C/K)

Use the following two initial words, repeated spatially with period 14.
Displayed positions run from x=0 to x=13. Their integer encodings use
bit i for coordinate i.

```
X = (01110010011000)^infinity     integer 1614
Y = (11001000000100)^infinity     integer 2067
```

For clarity, use integer one-counts `C_T=T(1-Phi_T)/2`. Exact evolution
gives, at every spatial position,

```
C_4(X) = C_4(Y)
       = (2,2,3,2,2,2,2,1,1,2,2,3,1,1).
```

For the following four times, however,

```
C_4(F^4 X) = (1,3,3,2,1,2,3,2,2,3,3,1,3,2),
C_4(F^4 Y) = (3,1,3,0,3,3,2,2,0,2,2,2,3,1).
```

In particular,

```
Phi_4(X)_0 = Phi_4(Y)_0 = 0,
Phi_4(F^4 X)_0 = +1/2,    Phi_4(F^4 Y)_0 = -1/2,
Phi_8(X)_0 = +1/4,         Phi_8(Y)_0 = -1/4.
```

Since the **entire** Phi_4 fields agree, there is no deterministic map
of that field to either next field, even if the map may inspect every
spatial coordinate. This finite witness proves the universal assertion
false. A scan of larger times or periods is unnecessary for that claim.

The eight-row certificates are:

| t | F^t X | F^t Y |
|---:|---|---|
| 0 | 01110010011000 | 11001000000100 |
| 1 | 11001111110100 | 10111100001111 |
| 2 | 10111000000111 | 00100010011000 |
| 3 | 00100100001100 | 01110111110100 |
| 4 | 01111110011010 | 11000100000110 |
| 5 | 11000001110011 | 10101110001100 |
| 6 | 00100011001110 | 10101001011011 |
| 7 | 01110110111001 | 00101111010010 |

All entries and an additional output row were independently checked with
the unmodified ladder truth table. Spatial periodicity makes these
finite arrays exact infinite-width diagrams; there is no unverified tail.

**Finite minimality claim only.** Exhausting all 32,766 rows of widths
1 through 14 finds no such conflict at widths 1 through 13. At width 14
there are 16,335 distinct C_4 fields from 16,384 rows. There are 49
repeated-field rows, of which 28 have a different next field from the
first row retained for that field. The displayed pair is the first
conflict in increasing integer order. This establishes the smallest
periodic width, not minimality among nonperiodic configurations.

## 4. Finite support does not repair a fixed-radius closure (U/K)

For any proposed observation radius R, put `L=max(R+3,7)`. Define finite
rows X_R,Y_R by retaining the respective periodic words on [-L,L] and
putting zeros outside that interval.

By radius-one causality, their first four-step means on [-R,R] agree
exactly with the periodic examples: those means depend only on sites
[-R-3,R+3]. Their next four-step and eight-step means at zero also agree
with the periodic examples, since those depend only on [-7,7]. Therefore

```
Phi_4(X_R)|[-R,R] = Phi_4(Y_R)|[-R,R],
Phi_8(X_R)_0 != Phi_8(Y_R)_0.
```

This is a construction for **every** R, not a limit inferred from a
radius scan. It rules out a fixed-radius scale-doubling rule on the
mean field even when the class is restricted to finite-support initial
configurations. It does not show that either row occurs in the actual
lone-seed orbit; a seed-specific restriction remains a separate question.

There is an important distinction here. For every T>=1, Phi_T is
injective on any set of configurations having a common right tail.
Indeed, if two configurations have a rightmost discrepancy at d, left
permutivity makes their rightmost discrepancy at time t exactly d+t.
At coordinate d+T-1 the first T-1 time entries therefore agree and the
last differs. Their T-term integer sums differ by exactly one, so their
mean fields cannot agree everywhere.

Thus the complete mean field retains finite-support rows, but information
arbitrarily far away can be needed to compute the next mean near zero.
The finite cuts above agree on the prescribed mean window and differ
near its distant boundary. This injectivity argument also holds for
Rule 90 and supplies no density estimate.

## 5. Rule 90 and verification

The first-step Rule 30 inverse uses OR essentially. For Rule 90, the
period-three rows `111` and `001` both have first two-step one-count
field `(1,1,1)`, hence signed mean field zero. Their next two-step
count fields are respectively `(0,0,0)` and `(2,2,0)`. Thus even the
first mean is noninjective and has no autonomous evolution in Rule 90.
These are exact control configurations, not claims about its seed.

The unchanged `controls.rule90_control` passes its five cases
T=2,4,6,8,10. No part of this argument concludes half-density for the
Rule 90 lone seed, which has an eventually zero centre.

Reproduce:

```sh
uv run python experiments/rule30/p2_temporal_mean_closure.py
uv run python experiments/rule30/verify_p2_temporal_mean_closure.py
```

Artifacts:

- `experiments/rule30/p2-temporal-mean-closure.json`;
- `experiments/rule30/p2-temporal-mean-closure-independent.json`.

The independent verifier imports none of the producer's evolution,
averaging, decoder, or scan functions. It replays 32 decoder windows,
128+512+2,048 complete evolution windows, all 32,766 periodic rows,
and 261 mean coordinates across nine finite cuts. It performs
3,040,758 scalar cell evaluations and verifies the Rule 90 collision.
The producer's artifact SHA-256 is
`d0a472fc808c9b1c98405179530f5ea06b5d061c2609653f474f96235753ba41`.
Frozen engines were not changed.

## 6. What remains

The mean-only iteration tried here stops at a specific false step:
`Phi_4(x)` does not determine the field required to construct
`Phi_8(x)`. Call this the **four-step temporal-mean nonclosure**.
It is fundamental within that proposed state representation, including
every fixed observation radius on arbitrary finite-support rows.

P2 remains unresolved because no estimate `H_k=o(2^(2k))` for the
designated seed follows. A proof could retain additional temporal order
or boundary information and establish an inequality without an exact
mean-only evolution. This certificate does not rule that out. It also
does not prove non-automaticity or settle P1, and it establishes none
of the five requested P2 ladder rungs. All measured or enumerated
claims have their finite ranges stated; the all-radius obstruction
comes from the explicit causal-cut construction.
