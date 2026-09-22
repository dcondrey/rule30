# Exact inverse ambiguity and the remaining return gap

**Evidence:** U (symbolic automaton and fiber theorems), C (independent finite calibration). The proposed claim that every ambiguous right-row image is eventually periodic is false. This does not kill R1: the aperiodicity below is spatial, and no invariant temporal return set is constructed.

## 1. Exact ambiguity automaton

Fix the left boundary bit `a`, and write

```
G_a(x)_i = x_(i-1) XOR (x_i OR x_(i+1)),  i≥1, x_0=a.
```

For a predecessor define `q_i=2x_(i-1)+x_i`. If the target bit is `y_i`, then

```
q_i = f_(y_i)(q_(i+1)),
f_0 = (0,2,3,3),   f_1 = (2,0,1,1).
```

These tables follow directly from the OR rule and are checked against frozen `ladder.FWD`.

For two predecessors, use an unordered pair of states. There is an edge labelled `b` from `u` to `v` precisely when applying `f_b` to both entries of `v` and sorting gives `u`. Initially both entries must have first bit `a`. Diagonal states are allowed initially, since the predecessors may first differ arbitrarily far to the right. An accepting infinite path must eventually leave the diagonal. It can never return: equality of a later pair state would imply equality of every earlier state by the deterministic inverse recurrence.

This ten-state automaton, with eventual off-diagonal entry as its acceptance condition, characterizes **all** target rows with at least two distinct `G_a` predecessors. The characterization is exact in both directions. The state recurrence enforces the overlap of adjacent predecessor bits, and an unordered path can be consistently ordered after its first split. No independent exterior choices are introduced.

The off-diagonal transitions that can lie on an infinite path are:

| Current pair | Output bit | Next pair(s) |
|---|---:|---|
| `(0,1)` | 1 | `(1,2)` |
| `(0,2)` | 0 or 1 | `(0,1)` |
| `(0,3)` | 0 | `(0,2)`, `(0,3)` |
| `(1,2)` | 1 | `(0,2)`, `(0,3)` |
| `(2,3)` | 0 | `(1,2)` |

The omitted pair `(1,3)` has no outgoing edge. Pair `(2,3)` is transient; the other four productive pairs form the recurrent core. No three-edge path in that core has label `010`. Therefore every ambiguous target row **eventually avoids spatial `010`**. This is a necessary condition, not a sufficient replacement for the full automaton.

## 2. Aperiodic ambiguity exists explicitly

The core contains two loops at `(0,1)` with labels `110` and `111`. Hence there is a full binary block language of ambiguous targets, not merely periodic tails.

An explicit symbolic realization is the already known Cantor family:

```
y = (1,1,e_0)(1,1,e_1)(1,1,e_2)…,
a_(n+1) = 1 XOR a_n XOR e_n,
x = (a_0,1-a_0,0)(a_1,1-a_1,0)… .
```

Either choice `a_0=0` or `a_0=1` gives `G_0(x)=y`, by checking the three positions in each block. The two predecessors are distinct for every binary sequence `e`. Taking `e_n=v_2(n+1) mod2` makes `y` aperiodic. Indeed, for any proposed eventual period `p=2^s d` with `d` odd, choose arbitrarily large `m>s` of parity opposite to `s` and put `n=2^m−1`. Then `e_n=m mod2`, whereas `e_(n+p)=s mod2`. Periodicity of `y` would also make its every-third-bit subsequence `e` eventually periodic.

This is an exact spatial example. It does not establish a return: its source blocks are `010` or `100`, while its image blocks are `110` or `111`. The source and image sets are disjoint already in their first three cells. The subsequent return obstruction is recorded in [RESULTS-r1-cantor-return-gap.md](RESULTS-r1-cantor-return-gap.md).

## 3. Sharp finite fiber bounds

**U.** Every full infinite fiber of `G_a` has at most three elements. If four different predecessors existed, choose a coordinate beyond the first difference of every pair. Their four pair states would then be distinct forever. But either inverse map has image of cardinality three, so it cannot carry four distinct subsequent states to four distinct preceding states.

For three predecessors, the same argument gives a path on three-element subsets of the four states. Its only productive states and transitions are

```
{0,2,3} --0--> {0,1,2} --1--> {0,1,2} --1--> … .
```

Thus **three predecessors force the target to be eventually `1`**. In particular an aperiodic target has at most two predecessors. The aperiodic Cantor targets in section 2 have exactly two.

The bound three is attained for each boundary value. The same three right rows

```
100·(010)^∞,   010·(100)^∞,   011·(001)^∞
```

map to `110·1^∞` when `a=0`, and to `010·1^∞` when `a=1`. The finite seam and the three periodic tail positions verify these identities uniformly.

A finite bound on inverse fibers alone is not a temporal entropy or recurrence obstruction. In particular, the two-to-one aperiodic Cantor map above supplies no reason that a suitable larger return map must be impossible.

## 4. Verification and Rule90 control

Run:

```sh
uv run python experiments/rule30/r1-isolated-column/inverse_ambiguity.py
```

The adjacent JSON records the complete pair/triple graphs, sharp examples, and controls. A separately enumerated finite-row calibration checks 2,040 output words and 4,080 initial rows through output length 8, for both boundaries and both rules. It compares actual predecessor multiplicities with the diagonal-plus-distinct product automaton. The two symbolic Cantor branches receive 13,312 frozen forward-gate checks over all 256 eight-bit data words.

For Rule90, both inverse bit maps are permutations, and every target row has exactly two predecessors under either fixed boundary: choose the first right bit freely and solve the remaining odd/even ancestral chains recursively. Thus the OR-dependent rank-three and `010`-avoidance arguments do not transfer. The unchanged `controls.rule90_control(6)` passes all three cases. Frozen engines remain unmodified.

The precise unresolved step is a temporally closed return grammar. Spatial ambiguity is abundant, including for aperiodic rows; its images need not return to the source set under the required periodic drive. No proof or kill of R1 follows from these inverse facts alone.
