# Exact joint certificates for three capacity-18 seams

Date: 2026-09-13. **Partial extension: 15 of the 19 new exact-capacity-18
patterns have uniform mortality proofs. Four two-parameter patterns remain
open, including the requested `213(13)^a1213(13)^b03` family.**

No state cap or surviving residue is counted as a mortality certificate.
The completed patterns have sharp combined maxima `N=25` and `D=14`,
including their first two scalars. These are **not** bounds for the four
unresolved patterns, all of capacity 18, or unrestricted auxiliary states.
Period-two exclusion remains open.

## 1. Complete language coverage and the new finite bound

The [capacity-18 language audit](../../experiments/rule30/capacity18_language_audit.py)
filters the saved capacity-32 grammar and compares it with the actual
cap-18 inverse-count automaton. Its full labeled product closes at 126
states and 504 edges. Every acceptance label includes both chronological
guards, the two scalars, and the exact original fiber size. This proves an
all-length equality of languages, not a census of original words.

There are 32 patterns through capacity 18: the 13 patterns in the
[completed capacity-17 theorem](RESULTS-capacity17-mortality.md), plus
19 new patterns of exact capacity 18. The additions comprise two finite
exceptions, ten one-star patterns, and seven patterns with two independent
stars. The twelve simpler additions all have complete independent guard
certificates in [capacity18-simple-families.json](../../experiments/rule30/capacity18-simple-families.json).

One addition extends the attained lifetime from 24 to 25. For every `k>=0`,
the complete original fiber

```text
P 0^k S,
P in {30011,30030,30031,31011,31030,31031},
S in {1102,3002,3102}
```

has 18 members and second endpoint `30322(2)^k121032`, with initial tape
`01`. Each displayed prefix reaches the same two-layer column; an original
zero returns that column and emits `2`; each displayed suffix emits `1210`
and passes both terminal guards. The complete counted language proves that
these 18 originals exhaust the fiber at their fixed original length.

At `k=1692508`, the representative

```text
30011 0^1692508 1102,           original length 1692517,
tape 0111100011010111101111000, N=25, D=14
```

fails its next guard. The one-star proof closes the complete spatial
period, and a separate frozen-row implementation checks all residues and
all chronological births and guards.

Lifetime and repeat maxima are recorded separately. For example, the new
pattern with second bulk `30322(2)^k10` attains `N=12` at `k=740`, but
attains `D=4` at `k=484` with `N=11`. The new checker removes the unnecessary
assumption that one tape must attain both extrema; it preserves every
existing row, closure, and guard check. The old capacity-17 certificates
are unchanged.

## 2. What is closed jointly

For a fixed further temporal depth `n`, retain the entire spatial column

```text
q = (A_0, (A_1,B_1), ... , (A_n,B_n)).
```

Here the first pair belongs to the first bulk scan of the given second
endpoint; the appended birth triangle is handled separately. Let `T_w`
mean reading the actual spatial word `w` through every layer of this
column. Its recurrence is exactly the specified Z scan, including the
preceding input high bit. Starting from the actual prefix column, form

```text
O = { T_body1^a(q_prefix) : a>=0 },
S = { T_seam(q) : q in O },
J = { T_body2^b(s) : s in S, b>=0 }.
```

The primary engine closes `O`, transports **every** member through the
complete seam, and closes the union `J`. It stores complete columns and an
actual pair `(a,b)` for every joint state. It does not multiply two marginal
period bounds or restrict the parameters to a diagonal or rectangle.

The independent finite-state checker proves both directions:

1. Every first-orbit state is present and has the correct successor and
   eventual return. Every transported seam seed belongs to `J`, and every
   second-block successor remains in `J`. Induction covers every independent
   pair of nonnegative parameters.
2. Every listed `(a,b)` reaches its declared column, checked by exact powers
   of the independently reconstructed successor graph. There are no
   disconnected added components or fresh completions.

For each joint column it then reads the full fixed suffix. At temporal
layer `t`, it starts with the stored bulk pair, scans the entire length-`t-1`
birth suffix, tests `u=v`, and appends `3-s` only on a successful history.
It retains each earlier failed guard. Thus every tested scalar tape is
chronological, and no row-end predicate is substituted for the complete
history. A closed joint set with no history surviving the final depth is a
uniform theorem for that entire two-parameter family.

These are exact computational certificates with explicit closure arguments;
they are not proof-assistant formalizations.

## 3. Three complete two-parameter certificates

All displayed families are full second endpoints and have initial tape
`00`. Both parameters range independently over all nonnegative integers.
Pattern indices refer to the saved capacity-32 grammar.

| Index | Full second endpoint | Certified further depth | First-orbit states | Joint states | Max N | Max D |
|---:|---|---:|---:|---:|---:|---:|
| 5 | `21213(13)^a031(31)^b303` | 24 | 1048576 | 1048576 | 24 | 14 |
| 12 | `213(13)^a031(31)^b303` | 4 | 16 | 16 | 2 | 1 |
| 27 | `3031(31)^a3031(31)^b303` | 16 | 2048 | 2048 | 17 | 9 |

Every final joint set is closed and has zero survivors. The independent
checker verifies all seeds, joint transitions, parameter representatives,
complete tapes, and all chronological guards. Its implementation also
checks whole finite rows against the unchanged `panel/cert33.py` oracle.

The actual first failed further guard is 23 for index 5, 1 for index 12,
and 16 for index 27. The larger chosen construction depth in the first two
rows is harmless: it retains additional column coordinates, while the
guard checker stops each history at its first failure.

Artifacts: [index 5](../../experiments/rule30/capacity18-joint-05.json),
[index 12](../../experiments/rule30/capacity18-joint-12.json), and
[index 27](../../experiments/rule30/capacity18-joint-27.json).

There is also an all-temporal-depth explanation for these three closures.
The [exact seam intertwining identities](RESULTS-column-seam-intertwining.md)
show that each of these families has the same full guarded history as its
member with parameters `(a+b,0)`. The proof closes a vertical Mealy product,
including its ordered output, on every input column in the required
high-bit slice. It does not infer this reduction from the finite orbit
sizes in the table. The analogous global identity for the harder `1213`
seam fails already at depth one.

## 4. The four unresolved joints

The following rows record exact closed intermediate sets and an explicitly
incomplete next construction. They are not mortality proofs.

| Index | Full second endpoint | Last closed depth | Joint states at that depth | Surviving states | Next incomplete depth |
|---:|---|---:|---:|---:|---:|
| 8 | `21213(13)^a1213(13)^b03` | 8 | 16888 | 63 | 12 |
| 15 | `213(13)^a1213(13)^b03` | 12 | 441088 | 125 | 16 |
| 23 | `3031(31)^a213(13)^b03` | 12 | 365568 | 74 | 16 |
| 34 | `30322(2)^a100(0)^b32` | 8 | 30016 | 161 | 12 |

The last row has initial tape `01`; the others have `00`. Each incomplete
construction reached the declared two-million-state cap. Its guard
evaluation did not cover a complete joint set; a numerical zero in an
unevaluated field has no significance. The theorem flags are false.

The designated index-15 family is still unresolved, but a subsequent
[guarded first-return construction](RESULTS-guarded-two-block-lift.md)
has independently verified its exact survivor sets through depth 15.
It carries the actual ordered transport through skipped states on all
four new temporal-pair lifts and retains every admissible seam entry.

| Further depth | Reachable lifts before the new guard | Survivors after all guards | Transport-route records |
|---:|---:|---:|---:|
| 13 | 425 | 216 | 107008 |
| 14 | 703 | 351 | 340480 |
| 15 | 1088 | 545 | 1003008 |

These sets cover every independent `(a,b)` at their stated depth; they
are not a finite parameter rectangle. The depth-16 continuation reached the two-million-record transport-cache cap here; a later run (RESULTS-guarded-two-block-lift.md section 8) completed depth 16 under an 8,000,000-state route cap, 673 survivors. The surviving columns still preclude a mortality conclusion. In particular, the
small survivor sets do not by themselves compress the ordered transport
needed at the next depth. The
[independent verification](../../experiments/rule30/capacity18-guarded-15-independent.json)
explicitly certifies only the completed layers and leaves mortality false.

Two probes of the saved layers 13, 14 and 15 test ways to quotient the lift.
Both are finite observations on these three layers, not statements about
greater depths. For an old survivor `q`, the outcome is the pair (reachable new
sheets, live new sheets).

- A [pre-registered window test](../../experiments/rule30/PREREGISTRATION-seam15-suffix-quotient.md)
  keys the columns by their newest `k` temporal pairs. The least `k` that makes
  the outcome a function of the key is `11, 12, 13` at old depths `12, 13, 14`,
  which is `n-1` each time. No fixed-width window works, and the proposed
  width 6 fails in every layer. See
  [the artifact](../../experiments/rule30/seam15-suffix-quotient-probe.json).
- An [exploratory test](../../experiments/rule30/seam15_outcome_mechanism.py)
  keys the columns by the cycle monodromy of the lifted transport and by the
  mask of sheets that pass the new guard. Neither key determines the outcome,
  and neither does their pair: 8 of 27, 14 of 30 and 20 of 32 classes are
  mixed. The reachable sheets form a single monodromy orbit for only 17 of
  125, 48 of 216 and 54 of 351 columns.
- A [free-group cancellation probe](../../experiments/rule30/seam15_free_group_invariant_probe.py)
  keys the same three layers by a candidate topological invariant of the
  temporal-pair sequence: reduce it in the free monoid where adjacent pairs
  `1` and `2` annihilate, and take (residue length, XOR parity of the
  residue, original high bit). This mixes different outcomes in nearly
  every class: 17 of 22, 22 of 22 and 23 of 24 classes are mixed at old
  depths 12, 13 and 14. See
  [the artifact](../../experiments/rule30/seam15-free-group-invariant-probe.json).

The same run finds that the live sheets are exactly the reachable sheets
passing the guard mask. This is true by definition: cover liveness
(`steps == depth` after the suffix) and the mask (`accepts`) evaluate the
same guard predicate. Its content is narrower. Two separate implementations
of the predicate agree on every cover row, and liveness does no pruning
beyond that predicate. Any compression therefore has to act on the reachable
lift. Neither window keys nor monodromy compress it.

A [pre-registered contraction probe](../../experiments/rule30/PREREGISTRATION-body2-transport-contraction.md)
also rules out compressing the body2 transport itself through a small
nucleus. Each `13` block acts on the temporal tape as one tree automorphism
`g = s(0,1,1) o s(1,0,1)`, built from the letter machines of
[the seam report](RESULTS-column-seam-intertwining.md). The minimized
automaton of `g^n` has 9, 42, 169, 618, 2115, 6904, 21880, 67620, 205416,
614415 and 1811799 states for `n = 1..11`. Every one of these states lies on
a cycle. A state on a cycle is an element `h` with `h|_v = h` for a nonempty
`v`, and every such element belongs to the nucleus of a contracting group.
So if the group generated by the letter machines is contracting at all, its
nucleus has at least 1,811,799 elements. That is a proof. It is not a proof of
non-contraction, since the count has been computed only through `n = 11`.
The order of `g` on tree levels 1 to 10 is 2, 4, 16, 32, 32, 128, 256, 512,
1024, 2048, with no sign of finite order. Neither the power closure nor the
group nucleus iteration closed within ten minutes. See
[the artifact](../../experiments/rule30/body2-transport-contraction-probe.json).
The 1-to-11 power sweep replaced the pre-registered 256 powers, because the
automaton roughly triples with each power.

## 5. Reproduction and preservation

The new driver [two_block_family_certificate.py](../../experiments/rule30/two_block_family_certificate.py)
compiles [the joint-column engine](../../experiments/rule30/two_block_column_orbit.cpp)
and calls [the independent checker](../../experiments/rule30/verify_two_block_family.py)
only on a complete empty final joint set. Binary sidecars retain all full
columns and exact representatives. Source and sidecar hashes are recorded.

Verify a completed certificate without regenerating its joint set:

```sh
uv run --offline --no-project --with numpy python \
  experiments/rule30/verify_two_block_family.py \
  experiments/rule30/capacity18-joint-05.data/depth-24.json
```

The default driver invocation targets index 15 and currently returns an
explicit incomplete result. It must not be cited as a proof. The completed
certificates and the unfinished attempts are kept separately from the
previous capacity-17 artifacts. No old original-word census, GPU job, paid
computation, or singleton-seed prefix generation was run.
