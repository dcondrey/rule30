# The q14/T4 dyadic-reset prehistory obstruction

Date: 2026-09-09. Evidence: **U**, supported by a complete **C** check.
This strengthens the earlier finite-radius Rule 90 factor exclusions.
It does not prove R1 or exclude other source mechanisms.

## Uniform statement

Consider a Rule 30 factor whose finite input features come from the
lone-seed Rule 90 diagram, possibly at any fixed finite collection of
binary spatial/time scales. Suppose its external lookup clocks are
`t mod 4,x mod 14`; its centre is eventually periodic and zero at
phase 3 on its tail; and at times `t=3 mod 4` its neighbour copies or
complements the Rule 90 neighbour. No such
factor exists. The input features here use their current source times,
so all features around every fixed output site reset to zero just after
a sufficiently large dyadic pulse. Past-time features that remain
nonzero at this reset are not included in this statement.

Let `B_p` be the all-zero-input output row at clock phase `p`. Each
`B_p` is spatially 14-periodic, and `F(B_p)=B_(p+1 mod 4)`. Along
arbitrarily long source-zero intervals, every fixed output column equals
this background. Thus a periodic centre must agree with the centre of
`B` on its tail. The observed phase has `B_3(0)=0`.

Choose dyadic times `P` large enough to clear every fixed scale and
radius. At time `P`, source features tend pointwise to all zero as
`P` increases. At `P-1`, the original Rule 90 neighbour is one, whereas
its all-zero-input value is zero. The copy-or-complement condition
therefore requires the output neighbour to differ from `B_3(1)`.

Taking a convergent subsequence of the finitely many preceding rows
gives full two-sided rows `A_0,A_1,...` such that

```
F(A_0)=B_0,
F(A_d)=A_(d-1),
A_d(0)=B_(3-d mod 4)(0),
A_0(1)=1-B_3(1).
```

Only `d<=4` is needed below. The local Rule 30 equation passes to these
limits. One can equivalently use diagonal subsequence compactness on
these finitely many full rows; no periodicity assumption is made about
the unknown `A_d`.

## Complete inverse-row enumeration (U)

For a specified spatially `q`-periodic target row `y`, Rule 30 gives
the exact inverse recurrence

```
x_(j-1) = y_j XOR (x_j OR x_(j+1)).
```

Traversing one target period to the left defines a deterministic map
on the four possible pairs `(x_j,x_(j+1))`. Every two-sided preimage
induces a bi-infinite orbit of this four-state map. A bi-infinite orbit
of a finite deterministic map lies on a directed cycle: repetition
somewhere in its past puts its present and entire future on that cycle.
The preimage therefore has spatial period `m*q` for some `1<=m<=4`.
There are at most four preimages, one for each possible initial pair
on such a cycle.

The verifier enumerates the four seed pairs for each period `q,2q,3q,4q`
and deduplicates by the pair at sites 0 and 1. Thus it enumerates all
two-sided preimages, including any that were not initially assumed
periodic. The periodic inverse routine was independently calibrated by
enumerating every row at widths 1 through 8.

## Extinction certificate (C)

Exactly 31 rows of width 14 satisfy `F^4(B_3)=B_3`; 17 have centre bit
zero. Fourteen of these admit no preimage of `B_0` with the required
centre and changed neighbour. The other three give the following
complete backward reachable-set cardinalities:

| Background rows `(B_0,B_1,B_2,B_3)` as LSB-first integers | Centre clock | Counts at successive distances `d=0,1,...` |
|---|---|---|
| `(903,9417,16254,258)` | `1100` | `1,1,1,0` |
| `(15351,2064,7224,9804)` | `1000` | `1,1,1,1,0` |
| `(8127,129,8643,12900)` | `1110` | `1,0` |

The sets contain all full two-sided preimages at every step, filtered
only by the centre clock, and at the first step by the required changed
neighbour. All branches become empty. This finite complete check proves
the displayed prehistory system impossible, uniformly over every
factor radius and every included fixed binary scale.

An independent implementation using the frozen Rule 30 truth table and
four-state cycle maps reproduces all counts. It also identifies the
terminal forced preimages: the `1100` branch demands centre 1 but its
only next preimage is `8892` of period 14, with centre 0; the `1000`
branch demands centre 0 but its only next preimage is `3329` of period
14, with centre 1; the `1110` branch demands centre 1 but its only next
preimage is `118` of period 7, with centre 0.

Exact rows, periods, rejected preimages, and filter results are retained
in `dyadic-all-line-gate-T4-q14.json`. The earlier scale-2 calculation
with explicit source period bounds is in
`dyadic-backward-gate-T4-q14-scale2.json` and gives identical extinction
counts; those bounds are unnecessary in the strengthened argument.

## Rule 90 and scope

The inverse recurrence uses OR saturation. Its Rule 90 counterpart is
`x_(j-1)=y_j XOR x_(j+1)`, and the first exclusion already fails:
the zero row has the alternating preimage with centre 0 and neighbour
1. Its preceding Rule 90 rows can also retain zero centre, as seen by
taking the local limits of lone-seed rows immediately before larger and
larger dyadic times. Thus this argument does not exclude the Rule 90
template it was designed to test.

This is a uniform exclusion of the stated background-reset mechanism,
not of R1 or of automatic Rule 30 diagrams in general. In particular,
the Rule 150 source retains a central seed at dyadic times. Its reset
row is a finite perturbation of the background, so the periodic-target
inverse-row argument does not apply to that source.

Reproduce, from a fresh copy of the construction directory because
outputs are preserved:

```sh
uv run python dyadic_preimage_gate.py
uv run python dyadic_backward_gate.py
uv run python dyadic_all_line_gate.py
```
