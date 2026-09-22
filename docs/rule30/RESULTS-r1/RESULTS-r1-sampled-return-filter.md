# Sampled return-cover filter and its large-stride limit

**Evidence:** U (deduction from previously certified factors), C (exact finite graph computations). This does not prove R1, kill R1, or realize a new trace.

The proposed right-row construction seeks a nonempty compact set `K` such that

```
K ⊆ B^L(K ∩ [0]) ∩ B^L(K ∩ [1]),
```

where `B=G_1∘G_0` is the two-step map with centre drive `01`, and `[b]` fixes the current first right bit. Such a set would realize every binary sequence at rho sampling stride `L`. Existing forbidden factors therefore provide a necessary filter before constructing larger spatial automata.

## 1. Exact small-stride obstructions

The input is the independently checked cumulative avoidance graph in [RESULTS-r1-cumulative-factor-obstruction.md](RESULTS-r1-cumulative-factor-obstruction.md): 57 minimal factors, 1,088 states, and one recurrent component with 811 states and 1,028 edges. Its inherited factor burn-in is 23 rho samples.

For a fixed stride, a labelled transition takes a specified first edge followed by `L-1` unrestricted edges. Exact subset construction starts from every recurrent state. An empty subset gives a missing sampled word. It is an obstruction in a necessary relaxation, so no realization is inferred from surviving paths.

| Stride L | Shortest word absent from recurrent projection | Subsets visited | Transitions examined |
|---:|---|---:|---:|
| 4 | `1011` | 24 | 26 |
| 5 | `1011110101` | 328 | 516 |

A separate set-based replay checks each word. To avoid any issue about when a path enters the recurrent component, both words were doubled and replayed from **all 1,088 states**, with no unrestricted trailing cells after the final observed bit. Both extinguish that complete graph. For stride 4, extinction already occurs on prefix `10111`, at rho offsets `0,4,8,12,16`. For stride 5, the doubled word is `10111101011011110101`, at offsets `0,5,…,95`. These are sufficient finite masks after the inherited burn-in; no claim that these full-graph masks are shortest is made.

Earlier direct core masks already exclude arbitrary sampling at strides 2 and 3:

- `1?0?1?0?1`, observing `10101` at stride 2;
- `1??0??1??1`, observing `1011` at stride 3.

These exclusions kill the specified full-binary-cover proposals. They do not exclude a return construction with a constrained aperiodic observation language.

## 2. Explicit return words pass stride 19 and every stride at least 35

**U/C.** The stored hub 54 has loop `A=00100001010101010` of length 17 and loop `B=10` of length 2. The two words `AB` and `BA` both return to this hub, have equal length 19, and begin with opposite bits. Arbitrary concatenations of these two loops therefore realize every sampled binary sequence at stride 19 in the avoidance graph.

Append `B^a` to both return words to obtain every odd stride at least 19. Append `A B^a` to both to obtain every even stride at least 36. In particular, **every stride at least 35 passes the current factor-language filter**. These are explicit graph walks, so no stride census or extrapolation is involved. They do not supply actual right rows.

## 3. Uniform connections between arbitrary graph states

**U/C.** The graph's stored hub 54 has actual closed walks of lengths 2 and 17. Independent breadth-first distances give:

- every recurrent vertex reaches the hub within 22 edges;
- the hub reaches every recurrent vertex within 191 edges.

Every integer at least 16 is `2a+17b` with nonnegative integers `a,b`: an even integer uses only the length-2 loop; an odd integer is at least 17 and uses one length-17 loop. Consequently, for any recurrent vertices `v,w` and any exact length `k≥229`, travel from `v` to the hub, use the two hub loops, then travel to `w`. The residual length is at least `229−22−191=16` and has the required decomposition. The code checks all 657,721 ordered pairs and validates both stored loop words and the distance certificates.

Thus the recurrent adjacency matrix is positive at every power at least 229. To realize any chosen sampled bit word in this *graph*, select an edge with each desired bit and connect consecutive selected edges by `L−1` intermediate edges. This works whenever `L≥230`. Compactness, or explicit repeated choices of these finite graph paths, also yields every infinite sampled binary sequence in the graph relaxation.

This is a uniform limit on the **existing factor filter**, not a realizability theorem. A spatial return construction at a large stride could still fail for other reasons. Conversely, small-stride exclusions cannot be extrapolated to exclude all sampled return covers.

The requested adjacency-power diagnostic stopped at its stated cap of 100: no positive power had been found, and rows reached between 688 and 712 of the 811 vertices. The constructive bound above replaces further power enumeration. It is not claimed to be the least positive exponent.

## 4. Reproduction and independent engine audit

Run from the repository root:

```sh
uv run python experiments/rule30/r1-isolated-column/sampled_factor_projection.py --stride 4
uv run python experiments/rule30/r1-isolated-column/sampled_factor_projection.py --stride 5
uv run python experiments/rule30/r1-isolated-column/factor_graph_mixing_bound.py
uv run python experiments/rule30/r1-zero-set-attack/construction/verify_sofic_return_cover_independent.py
```

The first three commands save their exact counts and source SHA-256 in adjacent JSON files. The cumulative input SHA-256 is `bf773b8333368a0c65df55f3c9b8fcb620292bab259a32c751593d63e95679fd`.

The independent spatial-language engine audit uses a different productivity calculation, complete subset languages, and all-word product searches. It checks 773 raw NFAs through two states, 9,276 exact image identities, 51,076 inclusion pairs, and 51,076 intersection pairs. It also checks all 86 raw partial DFAs through two states and 1,032 exact image identities. These are finite implementation audits, not an all-size software correctness theorem.

The Rule90 control admits both branch covers for drives `01`, `0101`, and `010101`, giving six exact positive checks. The Rule30 mask restrictions are inherited from the OR-dependent certified cones; they are not applied to Rule90. The unchanged `controls.rule90_control(6)` was also run and recorded in the independently checked trace-transitivity artifact linked below. No frozen engine was edited.

## 5. Scope

A nonempty exact fixed point of the compact return-cover operator would be sufficient: construct a forward segment for each finite requested observation word by choosing predecessors in reverse order, then intersect the nested compact initial-row constraints. This correctly produces a forward orbit, without mistaking an arbitrary infinite past for the desired forward itinerary.

No such Rule30 fixed point has been found here. These results exclude specified strides for unrestricted binary observations, audit the exact image/intersection machinery, and prove that the current finite-factor relaxation cannot exclude all larger strides. The actual recurrent trace gluing obligation in [RESULTS-r1-trace-factor-transitivity.md](RESULTS-r1-trace-factor-transitivity.md) remains unresolved.
