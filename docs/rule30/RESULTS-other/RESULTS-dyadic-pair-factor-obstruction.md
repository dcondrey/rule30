# Exact two-step Rule 30 evolution retains all four spatial pair states

Date: 2026-09-10. **Exact local identities and a complete factor obstruction;
P1, P2, and P3 remain unresolved.**

The Duhamel residual suggests grouping two time steps so that the Rule 150
propagator separates into its even and odd spatial lanes. This audit retains
the actual Rule 30 nonlinear feedback during that grouping. There is a compact
exact two-step rule, but no proper nonconstant projection of the four pair
states closes under it. The classification includes pair parity, the `11`
defect indicator, either individual bit, and every three-symbol projection.

This is a complete result for a specified representation, not an obstruction
to every renormalization or to inequalities that do not require exact closure.
Rules 90 and 150 both pass the matching closure test.

## 1. The nonlinear two-step equation

Let `a,b,c,d,e` denote the input bits at positions `i-2,...,i+2`.
Writing all sums in GF(2), direct composition gives

```
F30^2(x)_i
 = a+d+e+bd+cd+be+ce+de+bde+cde
 = a+(1+b+c)(d+e+de).
```

Equivalently,

```
F30^2(x)_i
 = x_(i-2) XOR
   [(1 XOR x_(i-1) XOR x_i) AND (x_(i+1) OR x_(i+2))].       (1)
```

The complete truth table has only 32 assignments; the verifier checks all of
them independently against two scalar Rule 30 updates. Unlike the linear
Rule 150 identity `L^2 x_i=x_(i-2)+x_i+x_(i+2)`, equation (1) retains both
spatial parities and has nonzero cubic terms.

At even times, set

```
e_m=x_(2m),    o_m=x_(2m+1).
```

Then two Rule 30 steps give the exact four-state, radius-one coarse rule

```
e'_m = e_(m-1) XOR
       [(1 XOR o_(m-1) XOR e_m) AND (o_m OR e_(m+1))],

o'_m = o_(m-1) XOR
       [(1 XOR e_m XOR o_m) AND (e_(m+1) OR o_(m+1))].       (2)
```

The four-state description is simply the original row grouped into spatial
pairs. The classification below asks whether any information in those pairs
can be discarded while preserving autonomous evolution of the projected
field.

For comparison with the residual, let `Q^t` be the actual nonlinear source
with the mandatory left-edge source removed, and let `U^t` be its accumulated
Rule 150 response. The exact relation is

```
U^(t+2)=L^2 U^t XOR L Q^t XOR Q^(t+1).
```

The last two terms retain the nonlinear feedback. For the full state the
corresponding identity is

```
F^2(x)=L^2 x XOR L N(x) XOR N(F(x)).
```

Equation (1) results by evaluating this full-state feedback exactly, rather
than treating the source terms as independent noise or deleting them through
a scaling assumption.

## 2. Definition and complete classification of pair projections

A pair projection `pi` assigns a symbol to each state in the ordered list

```
00, 01, 10, 11.
```

Only the partition into equal-output classes matters; renaming the output
symbols changes no closure property. There are 15 partitions of four states:
one constant partition, seven two-class partitions, six three-class partitions,
and the four-singleton partition.

A radius-one projected evolution would require

```
pi((F^2 x)_0,(F^2 x)_1)
 = K(pi(x_-2,x_-1), pi(x_0,x_1), pi(x_2,x_3))              (3)
```

for some function `K`. For each of the 13 proper nonconstant partitions, the
table below gives two six-bit input windows with the same projected input
triple and different projected output. Thus none satisfies (3).

The first column lists the four projection labels in order `00,01,10,11`.
For example, `0001` is the `11` defect indicator, `0011` retains the first bit,
`0101` retains the second bit, and `0110` is pair XOR.

| Projection | Input windows | Common projected input | Different outputs | Even seed times |
|---|---|---|---|---|
| 0001 | 001000 / 100001 | 000 | 0 / 1 | 0 / 6 |
| 0010 | 110010 / 001110 | 001 | 1 / 0 | 2 / 8 |
| 0011 | 110010 / 100110 | 101 | 1 / 0 | 2 / 12 |
| 0012 | 010111 / 000011 | 002 | 0 / 2 | 10 / 20 |
| 0100 | 001000 / 001110 | 000 | 0 / 1 | 0 / 8 |
| 0101 | 001110 / 100110 | 010 | 1 / 0 | 8 / 12 |
| 0102 | 110010 / 111010 | 200 | 0 / 1 | 2 / 16 |
| 0110 | 111010 / 111001 | 011 | 1 / 0 | 16 / 26 |
| 0111 | 010111 / 100110 | 111 | 1 / 0 | 10 / 12 |
| 0112 | 111010 / 111001 | 211 | 1 / 2 | 16 / 26 |
| 0120 | 110010 / 001110 | 002 | 2 / 1 | 2 / 8 |
| 0121 | 010111 / 011111 | 111 | 1 / 2 | 10 / 24 |
| 0122 | 111010 / 101010 | 222 | 1 / 2 | 16 / 64 |

The windows occupy physical coordinates `-2,-1,0,1,2,3`. Two updates determine
the complete output pair at coordinates `0,1`, so no unspecified exterior
cell can affect any displayed output.

**Universal consequence, including nonlocal maps.** For a given collision,
extend both six-bit windows by zeros to complete finite-support configurations.
Their projected fields agree everywhere: they agree on the three displayed
pairs and are equal outside. Their next projected fields differ at the central
pair. Therefore no deterministic evolution of the complete projected field,
even a nonlocal one, exists for that projection on all configurations.

**Seed-specific consequence, restricted to radius one.** Each listed window
occurs at coordinates `[-2,3]` of the actual lone-seed orbit at the even time
shown. Thus a time-homogeneous radius-one function `K` cannot satisfy (3) for
the entire orbit from its start. All 13 witnesses use input times at most 64
and output times at most 66. These are the earliest collisions detected in
increasing even time for each projection. The certificate also includes the
separate lexicographically selected universal witnesses, realized at even seed
times at most 302.

This does not exclude a larger neighborhood on the seed orbit, because the
projected fields outside the listed windows need not agree at the two seed
times. It does not exclude eventual closure after an unknown cutoff: no
arbitrarily late recurrence of these collisions is proved.

As an additional finite completeness check, every one of the 64 possible
six-bit central windows occurs at an even seed time by 566. This observation
is about length six only and proves no all-length language theorem.

## 3. Linear controls close at the same scale

For Rule 90,

```
F90^2(x)_i=x_(i-2) XOR x_(i+2).
```

For Rule 150,

```
F150^2(x)_i=x_(i-2) XOR x_i XOR x_(i+2).
```

Therefore the even lane and the odd lane separately follow the original rule
on the coarse lattice. By linearity their XOR does as well. Exhausting the
same 15 partitions confirms that both controls have exactly three proper
nonconstant closing projections:

```
0011: first bit;
0101: second bit;
0110: pair XOR.
```

The induced binary rule is respectively Rule 90 or Rule 150. The constant and
four-singleton partitions also close, as expected. No three-class partition
closes for either control.

This distinguishes Rule 30 from these linear controls at the first spatial
and temporal doubling. It does not turn the distinction into a discrepancy
estimate or an algorithmic lower bound.

## 4. Relation to previous nonclosure results

Exact block coarse-graining is an established approach. The framework and
larger finite searches are described by
[Song and Grochow](https://www.cs.toronto.edu/~jgrochow/songGrochowCA.pdf),
building on Israeli and Goldenfeld. Their paper studies binary target rules
through block size seven and leaves arbitrary-size nonexistence questions
open. [Dzwinel and Magiera's published abstract](https://doi.org/10.1016/j.jocs.2015.07.001)
also identifies Rule 30 among the remaining cases at size seven. This report
provides explicit local certificates and their actual-seed occurrences;
it makes no priority claim for finite coarse-graining nonexistence.

The [temporal-mean report](RESULTS-p2-temporal-mean-nonclosure.md) proved a
different obstruction: four-step temporal means of entire rows can agree
while the next means differ. Its first two-step mean has a local inverse.
Here the observed objects are spatial pairs at one instant, projected to two
or three symbols, and the first two-step evolution already fails to close.

The [dyadic grammar report](ARM7-dyadic-spacetime-grammar.md) records finite
compression diagnostics but no bounded grammar. The present classification
does not revisit those measurements; it gives a complete answer for one
small, specified state family.

The [Walsh/tree-energy reduction](RESULTS-p2-time-index-walsh.md) still requires
a seed-specific sublinear cancellation estimate. An inequality may succeed
without autonomous pair closure. Retaining larger blocks, an evolving state
alphabet, or absolute phase is also outside this obstruction.

## 5. Reproduction and evidence

Run from the repository root:

```sh
uv run python experiments/rule30/dyadic_pair_factor_audit.py \
  --output experiments/rule30/dyadic-pair-factor-audit.json
```

The audit checks:

- all 32 assignments for the compact two-step identity;
- all 15 pair partitions, with an explicit collision for each rejected one;
- the matching complete partition classifications for Rules 90 and 150;
- 569 complete lone-seed rows using both a packed-integer recurrence and an
  independent scalar set evolution;
- each recorded central witness and its two-step output on the actual seed;
- all 64 length-six central words and their first even-time occurrence.

The [JSON certificate](../../experiments/rule30/dyadic-pair-factor-audit.json)
contains every projection, witness, seed time, and control classification.
No extrapolation in time is used for the closure obstruction: the exhaustive
local collisions prove the universal statement and their actual seed
occurrences prove the stated seed-specific radius-one obstruction.
