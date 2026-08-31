# ARM8: center-observational quotient

## Status

The tested reduced ordered decision-diagram route grows exponentially and is
closed for the measured variable orders.  It does not rule out a different
query-specific algebra or a shortcut specialized to the single-seed orbit.

## Motivation

The challenge requests one center bit, not the full spacetime diagram.  ARM7's
exact tile grammar may therefore retain irrelevant interior information.  For
horizon `h`, define the Boolean function

```text
F_h : {0,1}^{2h+1} -> {0,1}
```

that maps an arbitrary causal input row to its center cell after `h` Rule 30
steps.  A reduced ordered binary decision diagram (ROBDD) canonically merges
partial inputs that have the same remaining effect on that query.  Its width
at a variable cut is an exact observational-state count for that order.

`experiments/rule30/center_function_probe.py` constructs `F_h` symbolically
from the local rule, structurally interns every decision node, and reports only
nodes reachable from the final center function.  It tests left-to-right,
right-to-left, center-out, outside-in, and bit-reversal orders.  Exhaustive
truth-table tests at horizon 2 compare Rules 22, 30, 90, and 110 against an
independent direct evaluator.

## Results

Rule 90 is the positive control.  In right-to-left order its reachable diagram
has 3--15 nodes through horizon 16 and maximum width 2, as expected from its
linear self-similarity.

Rule 30 is strongly order-sensitive.  At horizon 12:

| variable order | reachable nodes |
|---|---:|
| right to left | 4,836 |
| center out | 23,821 |
| left to right | 36,651 |
| outside in | 132,209 |
| bit reversal | 229,857 |

The winning right-to-left order extends as follows:

| horizon | reachable nodes | maximum width | nodes allocated while constructing |
|---:|---:|---:|---:|
| 2 | 7 | 2 | 24 |
| 4 | 28 | 7 | 172 |
| 6 | 105 | 24 | 869 |
| 8 | 405 | 92 | 3,845 |
| 10 | 1,433 | 315 | 15,499 |
| 12 | 4,836 | 1,118 | 58,019 |
| 14 | 15,543 | 3,706 | 204,847 |
| 16 | 47,909 | 11,984 | 684,324 |

A log-linear fit over these points gives an empirical exponential base of
about 1.88 per time step for total reachable nodes.  The construction hits its
two-million-node allocation guard at horizon 18.  A power-law fit is not a
credible explanation of this rapidly rising sequence.

The directional advantage is real and consistent with Rule 30's asymmetric,
left-permutive local formula

```text
next = left XOR (center OR right).
```

But changing direction reduces the exponential base/constant rather than the
observed growth class.

## Boundary of the result

This probe excludes only the five tested fixed variable orders for an ROBDD of
the arbitrary-input transfer function `F_h`.

- A shortcut for the one-seed orbit need not represent every possible input
  row, so `F_h` can be a stronger state than necessary.
- A different circuit, algebraic decision diagram, tensor factorization, or
  context-dependent variable order may be smaller.
- Finite exponential growth is evidence, not an asymptotic lower-bound proof.
- Building the diagram symbolically is itself expensive and supplies no
  dyadic construction law.

The next candidate must exploit the right-to-left asymmetry while restricting
state to contexts reachable from the single-seed orbit.  It must still define
an exact doubling operation; naming an alternative diagram formalism without
that operation is not progress.

## Reproduction

From `experiments/rule30`:

```bash
uv run python -m unittest test_center_function_probe.py
uv run python center_function_probe.py \
  --rules 90 22 30 110 --horizons 2 4 6 8 10 12
uv run python center_function_probe.py \
  --rules 90 30 --horizons 2 4 6 8 10 12 14 16 \
  --orders right_to_left --max-nodes 2000000
```
