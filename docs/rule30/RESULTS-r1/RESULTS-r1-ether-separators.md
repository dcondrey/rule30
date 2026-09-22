# Moving-ether separator rigidity

Date: 2026-09-09. Evidence: **U** (restricted-class uniform exclusion),
**C** (complete finite-state checks). This is an intermediate construction
filter, not a proof or kill of R1.

## Mechanism and exact scope

With the least significant bit at spatial position 0, put

\[
 K(a)_x=a_{x-2}\oplus(a_{x-1}\lor a_x).
\]

Thus `K` is Rule 30 followed by a shift toward increasing spatial
coordinates. The ring-8 ether has the five-step `K` cycle

```text
7 -> 19 -> 123 -> 18 -> 126 -> 7.
```

Every block has bit 7 equal to zero at every phase. In the original Rule
30 coordinates these zeros follow moving lines; they are not a fixed
centre-column clock. The construction tested here preserves **all** these
zero lines: `K^t(a)_(8j+7)=0` for every `j` and `t>=0`.

The mechanism is an exact partial map on eight-cell blocks. Its kill
condition is extinction of a right-continuation branch after all possible
block states have been included. That condition fires: if the initial row
agrees with the phase-0 ether on a left half-line, preserving every zero
separator forces the entire row to be the pure phase-0 ether. In
particular, no nonzero finite defect of this ether preserves every
separator. Defects that change a separator are outside this result.

## Deriving the block alphabet (U)

Write an eight-cell block as `(a,b,c,d_3,d,y,z,0)` and let `u` be bit 6
of the preceding block. The next separator bit is `y xor z`, so every
valid block has `z=y`. Equality of the next bits 5 and 6 then forces
`d_3=d*y`. Requiring this last relation at the following time gives

\[
 b=d\lor(c\land\neg y).
\]

Thus every block at every time belongs to the following 16-state set:

\[
 a+2\bigl(d\lor(c\land\neg y)\bigr)+4c+8dy+16d+96y,
 \qquad a,c,d,y\in\{0,1\}.
\]

The next block is completely determined by this state and the preceding
block's bit 6. Allowing that input independently to be 0 or 1 gives an
overapproximation, so it includes every actual separator-preserving
diagram. Removing states with no possible infinite future gives exact
set sizes `16 -> 11 -> 9`. The remaining transition table is:

| State | Input 0 | Input 1 |
|---:|---:|---:|
| 0 | 0 | 1 |
| 1 | 7 | absent |
| 7 | 19 | 18 |
| 18 | 126 | absent |
| 19 | 123 | absent |
| 96 | 96 | absent |
| 101 | 123 | absent |
| 123 | 19 | 18 |
| 126 | absent | 7 |

An absent transition is incompatible with an infinite future preserving
the separators. No spatial periodicity has been assumed in this table.

## The complete right-continuation calculation (U supported by C)

Let `Y(t)` be bit 6 of the pure five-phase ether. Its period word is
`00101`. A driver defect set `D` means the actual input to a block is
`Y(t) xor 1_(t in D)`.

For each driver below, the verifier tries every one of the nine initial
block states. After the last driver defect, the pair `(time mod 5,state)`
is a finite autonomous system. Each trajectory is followed until it
repeats a pair or encounters an absent transition; this decides its
entire infinite future, rather than checking a chosen time horizon.

| Input driver defects | All initial states with an infinite future | Resulting bit-6 driver defects |
|---|---|---|
| none | 7; 123 | none; `{0}`, respectively |
| `{0}` | 0 | `{2}` |
| `{2}` | none | no continuation |

Suppose a row with a pure ether left half-line first differs at block
`j`. The first row of the table forces block `j` to start in state 123.
The second row then forces block `j+1` to start in state 0. The third
row says that block `j+2` has no possible state. This is a contradiction.
It applies to any right tail, finite or infinite, and proves the stated
uniform exclusion.

## A second restricted check: keeping the constant-one sites

If one also requires every bit `8j+1` to remain 1, the alphabet reduces
to the five ether states. To check two adjacent blocks, a vertex is their
ordered pair of states, and an edge allows either input bit immediately
to their left while updating both blocks consistently. This graph has
25 vertices and 25 edges. Pruning vertices without an infinite future
gives `25 -> 18 -> 13 -> 9 -> 7`. The survivors are the five diagonal
pairs and `(7,123)`, `(123,7)`; every surviving edge enters a diagonal
pair in one step.

Consequently all blocks are equal after one step, uniformly in space.
Each homogeneous ether row has exactly one homogeneous-compatible
preimage in this five-state alphabet. The original row was therefore
already a pure ether row. This stronger assumption rules out even an
arbitrary two-sided nonconstant block pattern.

## An individual doubling gate forbids the next separator (U/C)

The [doubling-latch lemma](RESULTS-r1-doubling-latch-recurrence.md) gives
an additional local restriction without assuming that all separators
survive. Suppose a recurrent prefix period doubles at coordinate `i`.
Then column `i-1` is identically 0, column `i+1` is identically 1, and
`X(t)=a_i(t)` satisfies `X(t+P)=1-X(t)` for the previous prefix period
`P`.

**Column `i+7` cannot be identically zero.** If it were, the eight-cell
block from `i` through `i+7` would have the two zero separators and the
constant-one site used above, so its recurrent temporal states would
belong to the five-state alphabet. Its temporal graph, permitting either
left input, is

```text
7 -> 19 or 18
19 -> 123
123 -> 19 or 18
18 -> 126
126 -> 7
```

In a periodic first-bit trace of this graph, each zero-run has exactly
length 2 (states 18,126), and every finite one-run has odd length
(one state 7, followed by zero or more pairs 19,123). The zero-free
19,123 cycle gives the all-one trace. None can be anti-periodic: a
half-period complement matches zero-runs and one-runs, which would
require the odd one-run lengths to equal 2.

The verifier independently checks this by taking pairs of graph states
whose first bits differ, and allowing their input bits independently.
This larger product graph has 12 vertices and 10 edges. Removing vertices
with no infinite future gives `12 -> 10 -> 6 -> 2 -> 0`. Thus even this
overapproximation admits no two infinite complementary first-bit traces.

For the five-phase width-8 ether, sufficiently far-right doubling gates
in a finite-perturbation recurrence would have to lie at multiples of
8, where the background has the required constant zero/one pair.
Precisely, if the initial discrepancy ends at `b`, a coordinate
`i>b+9` and its two neighbours are unaffected during the first five
background phases: the discrepancy can advance at most two sites per
step. A forced constant trace there must therefore agree with the
background in all five phases. Its only constant-zero and constant-one
columns are residues 7 and 1, respectively, giving `i=0 mod8`.
The lemma rules out doubling at two adjacent such gates `i` and `i+8`.
It does not rule out more widely separated gates, and it does not justify
assuming that the intervening separators are preserved.

## Exact checks and Rule 90 control (C)

The verifier independently checks the 16-state symbolic alphabet against
all 128 initial blocks with bit 7 zero and all eight length-3 input
words. It records all nine initial-state trajectories for each of the
three complete driver problems, including every failed update time.

The Rule 30 alphabet claim fails for Rule 90. The repeated block 85
(`10101010` when read from bit 0 upward) has every separator zero and
maps under the analogous `K_90` to the all-zero row, which remains zero.
Yet 85 is absent from the 16-state Rule 30 alphabet. The OR constraints
used in the derivation are essential. The companion verifier also runs
the unchanged `controls.rule90_control(6)`; all its recorded checks pass.

Reproduction commands, from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 experiments/rule30/r1-c011-seam/ether_separators.py
PYTHONDONTWRITEBYTECODE=1 python3 experiments/rule30/r1-c011-seam/verify.py
```

The exact transition and trajectory output is
[ether-separators.json](../../experiments/rule30/r1-c011-seam/ether-separators.json).
The new scripts do not modify any frozen engine.

## Honest scope

The exclusion concerns a specified moving-ether separator class. It does
not assert that arbitrary defects die, that the ether attracts every
initial row, that a fixed centre clock determines its neighbour, or that
all periodically driven right half-lines become periodic. Separator-
breaking scattering and all-depth recursive constructions remain open.
No statistic averaged over a spatial window is used, so the
single-column-overwrite statistic filter is not applicable. This
restricted construction filter establishes neither R1 nor its kill
condition.
