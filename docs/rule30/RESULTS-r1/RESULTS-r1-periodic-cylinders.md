# R1 intermediate result: the periodic-cylinder obstruction

Date: 2026-09-09. **Intermediate result; R1 and P1 remain open.**

Under the alternating centre drive `c_t = t mod 2`, there are explicit
104-cell and 124-cell initial right prefixes that force a periodic right
neighbour for **every infinite continuation of that prefix**. Their entire
prefixes return after 14 and 10 steps, respectively. The return is checked
over every relevant initial exterior assignment and then extended uniformly
by finite propagation and induction.

This refutes the proposed **NEPC** premise, “no nonempty initial-prefix
cylinder consists entirely of eventually periodic zero-set outputs.” It
does **not** refute R1: both displayed neighbours are periodic. The broader
search for an aperiodic neighbour under a periodic centre continues.

**Positive corollary, 2026-09-15:** these same cylinders give sharp
finite-left alternating-trace deadlines. A row with the 124-cell prefix
and no ones left of `-d` fails by time `d+7`; with the 104-cell prefix it
fails by `d+10`. The [proof and exact depth-dependent deadlines](RESULTS-r1-cylinder-deadlines.md)
use the forced torus left tail and hold for every right continuation.
This does not establish that the singleton enters either cylinder.

## Evidence ledger

| Claim | Level | Evidence |
|---|---|---|
| The displayed 124-bit prefix returns after 10 steps for every continuation | `C` + `U` | All 1,024 relevant initial tails checked; finite-cone locality and return induction |
| The displayed 104-bit prefix returns after 14 steps for every continuation | `C` + `U` | All 16,384 relevant initial tails checked; same induction |
| Corresponding zero-set traces are `(10000)^inf` and `(1010000)^inf`, of minimal periods 5 and 7 | `C` + `U` | Every return cone has the stated trace; both nonconstant words have prime length |
| NEPC and the global topological-transitivity proposal fail | `K`, uniformly | Two nonempty cylinders with incompatible periodic observable traces |
| No cylinder cycle preserved at every two-step block exists for the alternating drive | `U` | Exact safe-suffix gate and constant-one-column argument below |
| Loss of a determined prefix can be followed by its recovery | `C` | Nine-bit prefix `101010100`, 340 exact initial-tail assignments |
| Longer block search found no cycles in its specified finite range | `C` | 45,044 prefix cases; no extrapolation |
| R1 or the lone-seed P1 is proved or refuted | — | **Neither is established** |

Code and complete certificates:

* [`torus_prefix_cuts.py`](../../experiments/rule30/r1-isolated-column/torus_prefix_cuts.py)
  and [`torus_prefix_cuts.json`](../../experiments/rule30/r1-isolated-column/torus_prefix_cuts.json).
* [`prefix_blockers.py`](../../experiments/rule30/r1-isolated-column/prefix_blockers.py),
  [`prefix_blockers_r30.json`](../../experiments/rule30/r1-isolated-column/prefix_blockers_r30.json),
  [`prefix_blockers_r90.json`](../../experiments/rule30/r1-isolated-column/prefix_blockers_r90.json),
  and [`prefix_blockers_longblocks.json`](../../experiments/rule30/r1-isolated-column/prefix_blockers_longblocks.json).

## 1. The object and the two exact prefixes

Let `X = {0,1}^{N>=1}` be the right-infinite initial rows. Define the driven
half-line maps

```text
G_a(x)_i = x_(i-1) XOR (x_i OR x_(i+1)),    i >= 1, x_0 = a,
B = G_1 o G_0.
```

Thus `B` advances two ordinary Rule 30 steps with the centre prescribed as
`0,1,0,1,...`. For a finite word `u`, `[u]` denotes all infinite right rows
whose cells `1,...,|u|` equal `u`. Every string below is printed in increasing
spatial index, **cell 1 first**; it is not conventional most-significant-bit
integer notation.

The 124-cell prefix is

```text
1110011000001100100101010000010000101111111010001011000100101001010110110110010000010001010100011101011101000100110010101010
```

Call it `u_124`. Its certificate states

```text
B^5([u_124]) subseteq [u_124],
r_0...r_9 = 1101000100,
(r_0,r_2,r_4,...) = (10000)^inf.
```

The 104-cell prefix is

```text
10001100101111001011000111001001000111010100100100111110000100100001111011110000011111011000001010101100
```

Call it `u_104`. Its certificate states

```text
B^7([u_104]) subseteq [u_104],
r_0...r_13 = 11001101000100,
(r_0,r_2,r_4,...) = (1010000)^inf.
```

In particular, the tails may be all zero, all one, periodic, or aperiodic;
the assertions quantify over **all** tails, without imposing their future
values independently at different times.

These prefixes come from the existing spatial-period-155/time-period-10 and
spatial-period-728/time-period-14 tori in
[`RESULTS-ladder-rung2-periodic-realizability.md`](RESULTS-ladder-rung2-periodic-realizability.md).
Their periodic neighbour traces were already known. The new result is the
**open cylinder of arbitrary right continuations** sharing those traces.

## 2. Why the finite certificates prove the infinite statements

**Return lemma (`U`).** Fix a drive of period `T` and an initial prefix `u`
of length `N`. Suppose every one of the `2^T` rows `u v`, `v in {0,1}^T`,
has the same first `N` cells `u` after `T` driven steps. Then
`G_drive([u]) subseteq [u]` for the infinite half-line map.

*Proof.* In `T` radius-one steps, an output at a site at most `N` can depend
on no initial right site beyond `N+T`. Therefore the tested `T` exterior
bits include every possible influence on the returned prefix. The artificial
right edge of the finite calculation is never used: each step shortens the
computed row by one cell. The actual infinite row at time `T` again lies in
`[u]`. Apply the same argument to that row. Since the drive restarts in the
same phase, induction gives the return at every multiple of `T`. No
independence assumption is made about the actual tail at later times. QED.

For `u_124`, the independent full-row integer verifier exhausts `2^10 = 1024`
tails. For `u_104`, it exhausts `2^14 = 16384`. Every entire prefix returns:
**17,408 return checks, zero mismatches**. It also checks the displayed
column-1 trace during every return cone, with zero mismatches. Repeating the
cones proves the trace formula for all time. The symbolic induction, rather
than a long simulation, is the all-time step.

If a full Rule 30 diagram is wanted, each such driven half-plane has a
consistent left extension. Define columns successively leftward by

```text
s(t,x-1) = s(t+1,x) XOR (s(t,x) OR s(t,x+1)).
```

Each new column makes the Rule 30 equation at the preceding column hold at
every time. Recursion over `x=0,-1,-2,...` defines a genuine forward
space-time diagram. **No finite-left-support claim is made.** This extension
does not produce the aperiodic zero-set output required for an R1 kill.

## 3. How the cylinders were found, and exact minimality scope

The search first tested entire prefix graphs. For a drive of length `p`,
retain an edge `w -> v` precisely when all `2^p` initial exterior words give
the same `N`-bit output `v`. A directed cycle would provide an invariant
finite union of cylinders. This uses actual initial rows and ordinary
forward evolution, not an independently refreshed exterior boundary.

The first census covered drives `01`, `001`, and `011` at widths `1,...,20`:
**6,291,450 prefix cases and 41,943,000 initial-tail assignments per rule**.
There were no cycles. Rule 30 eligible-edge totals were respectively
786,432, 393,216, and 393,214. Rule 90 had no eligible edges.

The longer-block census used `(01)^h` with `h=2,...,6`, widths `1,...,12`,
and `h=7`, widths `1,...,11`. The declared cap was `N+2h <= 25` initial
bits per case. It checked **45,044 prefixes and 111,760,736 initial-tail
assignments**, finding no cycles. **This was a bounded diagnostic, not a
proof of NEPC.** The subsequently found prefixes are wider than that census.

The targeted search then checked every spatial cut of each of the four
known torus rows. For `N >= 2T`, exterior dependence after `T` steps is
confined to the last `T` output cells, whose relevant known input window
has length `2T`. That window repeats with the spatial period. Prefixes
`N < 2T` were checked directly. Thus this particular search covers every
prefix length of each of the four fixed phase-zero rows, for its specified
return time `T`.

| Torus time period `T` | Spatial period | Safe cut residues | Smallest safe prefix on this row |
|---:|---:|---|---:|
| 4 | 7 | none | none |
| 6 | 84 | none | none |
| 10 | 155 | 0, 1, 124, 125 | 124 |
| 14 | 728 | 1, 104, 338, 339, 416, 417, 651 | 104 |

There were **974 periodic cuts and 64 small prefixes**, with
**12,554,400 initial-tail assignments**. Each rejected cut has an explicit
counter-tail in the JSON and an independent scalar replay. The entire
prefix returns at the two selected successful cuts were then checked by
arbitrary-width integer evolution, independently of the numpy window test.

The width 104 witness is minimal **among these four fixed row/return-time
pairs**. It is not asserted to be the shortest cylinder among arbitrary
initial prefixes, phases, or return times.

## 4. Why a tempting two-step argument does not exclude these cylinders

There is a uniform, narrower result: no finite-width prefix cycle is
preserved at **every two-step application of `B`**.

For `N >= 3`, write the last three prefix cells as `d,a,b`. Exact local
calculation gives

```text
B([w]) has one N-bit prefix
    iff w ends in 01 or 010.
On such an edge, (B(w))_N = d, and d <= b.
```

The gate is checked over all 64 assignments of the six local input cells;
the remaining output cells cannot see the exterior. The last bit is
therefore nonincreasing along safe two-step edges.

In a cycle that bit is constant. If it is zero, every prefix ends `010`;
column `N-1` equals one at both microphases. If it is one, every prefix must
end `101`; column `N` equals one at both microphases. A column constantly
one forces the adjacent column on its left constantly zero by the pin,
then the next left column constantly one by the rule. Repeating forces a
fixed checkerboard all the way to column 0, contradicting its alternating
drive. The small graphs are explicit: for `N=1`, only `1 -> 0`; for `N=2`,
only `10 -> 00` and `01 -> 00`. This proves the stated all-width result.

It does **not** apply to a prefix returned only after `B^5` or `B^7`.
Knowledge of an entire fixed-width prefix can be lost and later recovered
through actual temporal correlations. The smallest example found in the
bounded longer-block scan was initial prefix `101010100`:

| Block time | All possible nine-bit prefixes | Initial tails exhausted |
|---:|---|---:|
| `B` | `001010101`, `001010100` | 4 |
| `B^2` | `010010101`, `010010100` | 16 |
| `B^3` | `000000101`, `000000100` | 64 |
| `B^4` | `100011001` | 256 |

These **340 assignments** are a direct finite-cone check. No global
minimality claim is attached to that example. The 104/124-cell cylinders
show that this recovery can participate in a recurrent return.

## 5. What precisely is killed

**Periodic-cylinder obstruction (`K`).** The proposed global NEPC property
is false: a nonempty open cylinder can force one periodic zero-set trace
for all its initial rows. Therefore the Baire-category plan that requires
every eventual-periodicity class to have empty interior cannot be applied
globally to this driven half-line.

The same witnesses rule out global topological transitivity of `B` on `X`,
and on `Omega(B) = intersection_n B^n(X)`. Every point in `[u_124]` has a
zero-set trace of period 5. After any number of `B` steps it still has a
5-periodic trace. No such point can enter `[u_104]`, whose trace has minimal
period 7. Both cylinders meet `Omega(B)`, since they contain their respective
periodic torus rows. These give two nonempty relatively open sets with no
forward transition from the first to the second.

This does **not** prove that every initial right row eventually enters a
periodic cylinder. It does not classify the complement of their basins, and
does not rule out an aperiodic output there. Restricting a later construction
to an appropriate invariant subset is an unresolved possibility.

## 6. Rule 90 and frozen-engine checks

The unchanged `controls.rule90_control(10)` was run at
`T=2,4,6,8,10`. All five bijectivity checks pass, and each constructed torus
passes its forward-rule check and achieves neighbour period `T`. Together
the exhaustive maps contain **1,118,480 states**.

The cylinder-return mechanism itself fails for Rule 90. After `T` steps,
the rightmost ancestral bit `x_(N+T)` occurs with coefficient one in the
output at `N`. Toggling that bit while fixing the prefix changes the
output. Thus no nonempty prefix cylinder can have a fixed returned prefix
after any positive number of steps. This is a uniform right-permutivity
argument; the finite Rule 90 census above confirms it in the reported
range. It is consistent with Rule 90's aperiodic lone-seed neighbour and
is not a proof of R1 for either rule.

Additional checks:

* Unmodified `numeric_rho`: each cylinder was sampled with an all-zero tail,
  64 ones followed by zeros, and 64 alternating bits followed by zeros.
  All six runs match their stated periodic word for 4,096 samples each:
  **24,576 checked rho symbols, zero mismatches**. These are checks of the
  uniform proof, not its justification.
* Unmodified ladder `FWD[30]`: **12,274 torus cells**, zero violations.
  The same complete tori were also checked through the unchanged torus
  verifier and an independent cyclic-row simulation.
* The prefix-graph engine agrees with independent scalar truth-table
  evolution on **140 complete small graphs**, covering both rules, all
  drives of lengths 1 through 3, and widths 1 through 5. Two
  constant-boundary cylinder controls are positive.
* All seven recorded source hashes in the prior rung-2 input manifest
  match, including `right_trace_forbidden.py`, `controls.py`, `torus.py`,
  and `ladder.py`. The ladder hash remains
  `589ab8443e8e61a604561823335d1066eeac5d6b093800a70e8d4a1f943ff96e`.
  Frozen engines and terminal-period machinery were not edited.

## 7. Reproduction and honest scope

From the repository root:

```sh
uv run python experiments/rule30/r1-isolated-column/torus_prefix_cuts.py
uv run python experiments/rule30/r1-isolated-column/prefix_blockers.py --max-width 20 --out experiments/rule30/r1-isolated-column/prefix_blockers_r30.json
uv run python experiments/rule30/r1-isolated-column/prefix_blockers.py --rule 90 --max-width 20 --out experiments/rule30/r1-isolated-column/prefix_blockers_r90.json
uv run python experiments/rule30/r1-isolated-column/prefix_blockers.py --max-width 12 --max-input-bits 25 --drives 0101 010101 01010101 0101010101 010101010101 01010101010101 --out experiments/rule30/r1-isolated-column/prefix_blockers_longblocks.json
```

The first command reproduces the new theorem and its controls. The later
commands reproduce the preceding bounded diagnostics and the correlation
counterexample; extending their census is unnecessary for the theorem.

Established: two explicit invariant cylinders, their uniform periodic
zero-set traces, and the failure of the global NEPC/transitivity premise.
Not established: R1, a kill of R1, any eventual-periodicity statement about
the lone seed, or exhaustion of all driven-half-line behaviours. **This
document records an intermediate obstruction; it is not the requested
proof-or-kill endpoint, and the R1 construction search continues.**
