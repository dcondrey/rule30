# P3: bounded decoders for the complementary field Q fail

Date: 2026-09-18. Tests the decoder classes left open by
[the two-channel blocking result](RESULTS-p3-b-two-channel-block.md)
section 4: recovering the complementary field Q^(L) from the primary field
P^(L), so that the index-halving step could iterate on P alone.

**Correction, same day.** The first version of this file overclaimed. It
said its class included "the whole ray", that it subsumed section 4's
phase-mod-16 witness, that a decoder supplied the full time index is "not a
lever", and that a sequential decoder is excluded by an O(j) streaming cost.
All four are retracted in section 6. Sections 1-5 replace it.

Fields throughout: (P^(L),Q^(L)) = S(B^(2L)(0)), split by equation (1) of
the two-channel result, from the exact zero ray with its state cycle closed.
The center column is the near-diagonal
c_(2h+e) = bit_e(digit_(h-1)(B^(h+1+e)(0))) of the same field
([actual B query](RESULTS-p3-actual-b-query.md)), re-verified here against
direct Rule 30 evolution for n=2..399 with zero mismatches. The query cone
is therefore j <= L.

## 1. Time information never rescues a window decoder

Within one ray every function of L is constant in j. At three macro times
Q's tail period does not divide P's, so no decoder
D(P_(j-w)..P_(j+w), tau(L)) can hold, for any fixed w and any tau,
including tau(L)=L:

| Macro time L | P tail | Q tail | p | q | tail starts at j/L |
|---:|---|---|---:|---:|---:|
| 37 | 3,3,3,3,... | 0,1,0,0,... | 1 | 4 | 56/37 |
| 44 | 2,3,2,3,... | 3,3,0,3,... | 2 | 4 | 64/44 |
| 74 | 2,3,2,3,... | 0,1,1,2,... | 2 | 4 | 120/74 |

A tail collision search confirms it at radii 0, 3 and 10 with no time
information, L mod 4, and the full L. Adding spatial phase j mod 4 removes
every tail collision; j mod 2 does not. These witnesses lie beyond the query
cone, and the query and any finite transducer both hold j mod 4 for free.
So this section shows only that Q needs spatial phase.

## 2. One blocking level, natural class

Pre-registered before its run: decoder input is a centered P window of
radius w, j mod s and L mod t, pooled over L=0..80 and every position from
j=0 to two tail periods past the transient. As a calibration, the fields
reproduce section 4's L=0/16 prefixes (P 00 and 00, Q 00 and 02). Section 4
derived those from the original binary generator, not this automaton. The
instrument also flags that pair as a collision.

| w | s=4: t=4 / 16 / 64 | s=8: t=4 / 16 / 64 |
|---:|---|---|
| 0 | collide / collide / collide | collide / collide / collide |
| 1 | collide / collide / collide | collide / collide / collide |
| 3 | collide / collide / collide | collide / collide / **none** |

Seventeen of eighteen settings collide, sixteen of them inside the query
cone. The one setting without a collision, w=3, s=8, t=64, has two repeated
keys in total, so it carries no information. At w=3, s=4, t=64 the single
collision is within the ray L=80, at j=22 and j=90. At that radius and time
modulus the data has no cross-time repeats, so larger time moduli need
longer runs of L to test at all.

## 3. Supplied full time index

Pre-registered before its run: within one ray L is fixed, so a within-ray
collision refutes D(P window radius w, j mod s, any function of L),
including the full L at unbounded cost. This is the no-cost form of the
[conditional decimation construction](RESULTS-p3-decimation-window.md),
whose correct fixed-radius law would give a polylogarithmic query. Kill:
two positions j, j' <= L in one ray with equal window and spatial phase and
unequal Q, over L=1..80.

| w | s=4 | s=8 | s=16 | first witness (s=4) |
|---:|---|---|---|---|
| 0 | 1662 of 2256 | 1169 of 1585 | 629 of 865 | L=6, j=0,4 |
| 1 | 228 of 317 | 125 of 168 | 46 of 67 | L=13, j=1,9 |
| 2 | 10 of 18 | 4 of 9 | 2 of 4 | L=36, j=13,33 |
| 3, 4 | no repeats | no repeats | no repeats | none |

Entries are colliding repeats of all in-cone within-ray repeats. **Refuted
for w<=2 with spatial phase mod 4, 8 or 16**, whatever the decoder does with
L. At w=0 and w=1 the collision rates 0.737 and 0.719 sit at the
independence baseline 0.749 = 1 - sum of squared in-cone Q frequencies
(0.269, 0.230, 0.262, 0.239). A window that short carries no information
about Q. The w=2 row rests on only 18, 9 and 4 repeats. Each collision
there is still an exact witness, but the instrument is at its power limit.
Radius 3 and above had no within-ray repeats by L=80.

**Longer rays.** A second pre-registered run takes the same kill to
L=1..2000. Its rays are generated incrementally, one B pass per step on a
fixed prefix, and that generator reproduces the L<=80 fields exactly before
any reading.

| w | s=4 | s=16 | first witness (s=4) |
|---:|---|---|---|
| 3 | 15017 of 20096 (0.747) | 3766 of 4989 (0.755) | L=117, j=26,38 |
| 4 | 996 of 1315 (0.757) | 258 of 325 (0.794) | L=266, j=15,179 |
| 5 | 58 of 83 (0.699) | 13 of 18 (0.722) | L=478, j=25,269 |

**Refuted for w<=5**, whatever the decoder does with L. The in-cone Q
frequencies are uniform within 0.002 (0.2511, 0.2495, 0.2499, 0.2495), so
the independence baseline is 0.750. Every rate sits there within sampling
error. The largest deviation, 0.794 on 325 repeats, is under two standard
errors. Out to radius 5, the P window carries no detectable information
about Q.

A positive control was added after the first run: a synthetic target,
the digit sum mod 4 of the radius-2 P window, run through the same
comparison loop. It gives zero collisions at every tested radius. The
instrument therefore reports a decoder when one exists; its 0.75 rates are
not an artifact of comparing unrelated positions.

## 4. Every level bounded would make the center column automatic

Call a renormalization of a(N,i) = digit_i(B^N(0)) bounded if one finite
stock serves every level. The stock holds finitely many transducers over
bounded alphabets, initial fields and readouts, and every kernel element
a(2^k L + r, 2^k j + s), with 0<=r,s<2^k, is one readout of one orbit from
it. Level k halves time and space together, which matches the 2D 2-kernel's
single shared exponent k. The kernel then has at most as many elements as
stock triples, so a is 2-automatic as a 2D sequence.

The even parity c_(2h) = bit_0(a(h+1, h-1)) is a diagonal at fixed offset
N-i=2, and the odd parity c_(2h+1) = bit_1(a(h+2, h-1)) one at offset 3.
Adding a constant is finite-state, so each fixed-offset diagonal is
2-automatic. So is a coding of it, and so is the perfect shuffle of two
2-automatic sequences. The center column would then be 2-automatic too.

[ARM6](../ARCHITECTURE/ARM6-binary-kernel.md), re-run here with the same
output, finds all 2^e residuals distinct through depth 12, 8191 in total.
Its Thue-Morse control holds at 2. Any 2-kernel consistent with 524288
center terms therefore has at least 8191 elements. Theorem O of
[the automaticity arm](../overnight/RESULTS-automaticity.md) says that is
the most such data can certify. Any stock must supply thousands of distinct
kernel elements. This covers every bounded-window, bounded-phase,
bounded-state decoder used at all levels, and it makes a level-by-level
witness hunt unnecessary for that class.

## 5. What stays open

A family that grows with the level or index while staying cheap, such as a
window radius or phase modulus increasing with k at polylogarithmic total
cost. Two results already in the repo bear on it. Non-automaticity is not a
P3 lower bound (`12067813fff0fe90`). The repo's triangular CA has a
non-automatic column with a cheap arithmetic query
(`r30-p3-triangular-ca-automaticity-query`). At level one, section 3 leaves
only decoders that read P beyond radius 5 or take an input other than a
centered P window. Radii 0 through 5 carry no detectable information. There
is no rising information curve to extrapolate. Extending the test to radius
6 or 7 needs rays to roughly L=4,000 and L=11,000 and is feasible, but the
flat curve gives no reason to expect a jump there.

## 6. Retracted claims

- "Any fixed radius, including the whole ray." A whole-ray decoder sees the
  origin and hence j.
- "Subsumes the phase-mod-16 witness." That witness is a prefix-region
  cross-time collision at j=0,1. The tail-period check cannot see it.
- "A decoder supplied the full time index is not a lever." The query always
  knows L. Section 3 tests that class directly.
- "A sequential decoder is excluded by its O(j) streaming cost." A
  bounded-state sequential decoder composes into the blocked transducer and
  is never streamed at query time. Section 4 covers the bounded case.
- The first version's "random-field control" was the rate at which random
  period pairs from {1,2,4} divide. It measured integer arithmetic, not
  fields. Section 3's independence baseline replaces it.

## Reproduction

`experiments/rule30/p3_two_channel_period_divisibility_probe.py`, `verify()`,
output saved to
`experiments/rule30/p3-two-channel-period-divisibility-probe.json`
(`tail_period_violations`, `phase_collisions_at_violations`,
`pooled_natural_class`, `supplied_L_within_ray_cone`). ARM6:
`uv run --no-project python experiments/rule30/automaticity_probe.py --identity-prefix 128 --rank-prefix 1024`.
