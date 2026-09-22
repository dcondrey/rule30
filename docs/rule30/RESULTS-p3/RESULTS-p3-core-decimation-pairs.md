# Exact tests of a shrinking core index by pair decimation

Status: **the specified static pair-blocking recursion is refuted on actual
seed-derived cores.** A terminal-only counterexample retains both boundary
bits and lies strictly inside the core. Separately, an exact periodic-bulk
certificate excludes a commuting version outside every fixed-width end
seam. Neither result excludes stateful decoders, nonlocal summaries,
different alphabets, or recursions preserving only the requested bit.

This tests a concrete way to advance the
[half-width core](RESULTS-p3-query-cone-rewrite.md) by a factor of two,
rather than treating one core update as free. The test generates the
cores from their constant-`C` initial words and retains their actual
boundary values `a=bit0(U(0)), b=bit1(U(0))` throughout.

## 1. The precise candidate

For `U=C u1...u_(2k)` of width `2k+1`, keep the leading `C` and group
the remaining letters into `k` disjoint pairs. A static pair code has form

\[
 \pi(U)=C\,\phi(u_1u_2)\,\phi(u_3u_4)\cdots
                 \phi(u_{2k-1}u_{2k}).                    \tag{1}
\]

The intended reduction is from the actual fine core
`Q^(2t)(C^(2k+1))` to the actual coarse core `Q^t(C^(k+1))`.
Requiring this for every `0<=t<=k` would give a commuting space/time
renormalization; requiring it only at `t=k` is a weaker terminal-only
candidate.

We allow the code to depend on the pair position modulo a specified
integer `d`, and to be selected using shared global metadata such as
`k,t,a,b`, or even additional information about the whole core. Within
one core it must still assign the same output to equal pairs at equal
position phases. We also distinguish a version allowing arbitrary output
exceptions in fixed-width regions at both ends.

This is a specified word-valued projection onto the existing shorter
`R/Q` core alphabet. It is not the class of all finite-state or
query-specific encodings. In particular, a decoder carrying state from
one pair to the next is outside (1), as is a method that obtains the final
scalar without reconstructing the shorter core word.

## 2. A terminal-only failure on one actual context

Take `k=16`. Exact evolution from the prescribed seeds gives

```text
Q^32(C^33) = CBCCCACBCCBCBCBCCABCBCCBCAACBCCBC
Q^16(C^17) = CBCCCACBCCBCBCCAB
```

Both final boundary pairs are `(a,b)=(1,0)`. Number the fine pairs by
`p=0,...,15`, so pair `p` occupies word positions `2p+1,2p+2` and
must produce coarse word position `p+1`.

| Position phase | Fine pair positions | Common input pair | Required coarse letters |
|---|---|---|---|
| modulo 2 | `4,6` | `CB` | `A,B` |
| modulo 4 | `5,9` | `CB` | `C,B` |

Each row gives two incompatible requirements on the same code entry,
inside the same actual context. Allowing the code to depend on the
entire shared boundary/time/width data cannot distinguish the positions.
The first row is outside four-pair end seams; the second is outside
five-pair end seams. Thus the terminal-only version of (1), with these
phase annotations and these seam allowances, fails exactly.

This counterexample does not assume correct projections at earlier times.
Its two final **root observables happen to agree**, so it refutes the
word projection, not a scalar center-query identity. Nor does this single
finite witness exclude every possible larger seam width.

## 3. An exact four-state bulk operator

Write `T(U)=U|_0`. Both finite core updates have the same first `L-1`
letters:

\[
 R(U),Q(U)=\operatorname{tail}(T^2(U))\ \text{followed by one boundary letter}.
                                                               \tag{2}
\]

Their appended letters differ in some cases and are always computed from
the actual `a,b`. Define a separate infinite-word bulk operator

\[
 D(U)=\operatorname{tail}(T^2(U)),                           \tag{3}
\]

on `C`-headed right-infinite words. We do **not** define `Q` or `R` on
such words by assigning a fictitious terminal scalar.

There is an exact four-state transducer for `T^2`. The state `s` is the
low-two-bit input that the next generator receives after the preceding
generators have acted. Reading the next generator emits its section at
that input and updates `s`:

| Incoming `s` | Emitted section, for any generator | Next `s` after `A` | after `B` | after `C` |
|---:|---|---:|---:|---:|
| 0 | `A` | 0 | 1 | 3 |
| 1 | `B` | 3 | 2 | 2 |
| 2 | `C` | 2 | 3 | 1 |
| 3 | `C` | 1 | 0 | 0 |

The equality of the emitted section across all three generators follows
by applying their binary-section recursions twice. The next-state columns
are their exact actions modulo four. Initialize `s=0` and discard the
first emitted letter to obtain `D`. A `C`-headed input makes that first
letter `A`, and the next letter `C`, preserving the required head.

**Prefix locality.** For either `F=R` or `F=Q`, after `r<L` steps from
`C^L`, the first `L-r` letters of `F^r(C^L)` equal the first `L-r`
letters of `D^r(C^infinity)`.

Proof: the first `j` letters of `D(U)` depend only on the first `j+1`
input letters. In one finite step, (2) agrees with that bulk through the
first `L-1` letters. Induct on `r`, reducing the protected prefix by one
letter per step. The appended letter may have its actual arbitrary
dependence on `a,b`; it lies outside the protected prefix at that stage.
This is a dependency proof retaining the real finite trajectories, not
a claim that their boundary values are freely interchangeable. QED.

## 4. Two closed product cycles give an all-seam obstruction

Compose three or six copies of the transducer in §3, discarding the first
output at each layer. After respectively three or six startup letters,
all deletions have occurred. Feed the constant input `C` forever.
The product-state trajectories close back to their initial states after
16 and 64 transitions, with no transient output prefix. The full state
cycles in the artifact therefore prove the exact periodic identities

```text
D^3(C^infinity) = (CACABCCCBCBCCAAA)^infinity

D^6(C^infinity) =
 (CBCCBCBCBCABCBCACACACBCABCBCBCBCBCCBCBCCABCBCBCBCBCCCBCBCCAAAAAA)^infinity
```

Cycle closure is an induction certificate: returning to the identical
complete product state under the identical constant input repeats every
subsequent output. It is not an extrapolation from a long sampled prefix.

Pair position `p` reads positions `2p+1,2p+2` in the second word and
should produce position `p+1` in the first. The resulting constraints
repeat every 32 pair positions. They contain these conflicts:

| Phase modulus `d` | Positions | Common pair | Required letters |
|---:|---|---|---|
| 1 | `1,2` | `CB` | `C,A` |
| 2 | `1,3` | `CB` | `C,B` |
| 4 | `1,13` | `CB` | `C,A` |
| 8 | `10,18` | `BC` | `C,A` |

**Theorem.** For any fixed end-seam allowance `M`, and any one of
`d=1,2,4,8`, no static pair code with phase modulo `d` produces the
coarse actual core from the fine actual core at every width and every
time along the proposed commuting recursion. This remains true if the
fine and coarse operators are independently chosen from `R,Q`, and if
the code is selected using arbitrary shared global metadata.

Proof: choose the appropriate conflicting positions `p1,p2` above.
Replace both by `p1+32z,p2+32z`, choosing `z>=0` so that both are at
least `M`. Their pairs, target letters, and phases are unchanged.
Choose

\[
 k=(p_2+32z)+M+4.
\]

Both positions then avoid the first and last `M` pairs and satisfy
`p<=k-4`. By prefix locality, their fine pairs after six actual steps
in width `2k+1`, and their coarse letters after three actual steps in
width `k+1`, equal the displayed periodic bulk. The two conflicting
requests therefore occur within one actual finite context, outside its
allowed seams. Shared metadata cannot resolve them. QED.

This all-seam theorem uses fixed fine/coarse times `6/3` while the widths
grow. It therefore concerns a projection required to commute along the
trajectories. It does **not** establish the same all-seam exclusion for
a terminal-only formula at `t=k`. The separate witness in §2 has that
weaker time requirement but only the stated finite seam margins.

At this fixed bulk depth, a phase modulo 16 has no conflicting code entry
in the displayed period. This is only a finite surviving condition, not
a proof that such a code works at another time or computes the query.
No larger phase search is performed.

## 5. Computation, cost, and scope

The [verifier](../../experiments/rule30/p3_core_decimation_pairs.py)
checks all twelve local transitions against the original binary-section
recursion and integer actions. It retains both complete product cycles,
requiring only 80 transitions after startup. Independent literal core
updates check the finite width-17/9 interior witness for both `R,Q`.
The directed terminal-only test performs 32 literal core updates at width
33 and 16 at width 17, with all intermediate words and actual boundary
bits saved. It constructs these words from `C^L`, rather than supplying
an arbitrary current state or a fresh continuation.

The [artifact](../../experiments/rule30/p3-core-decimation-pairs.json)
also preserves the smaller width-5 plain-code contradiction and all source
hashes. No frontier census, large prefix generation, paid job, or general
compression-growth measurement is involved.

```sh
uv run --offline --no-project python experiments/rule30/p3_core_decimation_pairs.py
```

A literal pair projection would itself cost linear work in the expanded
core. To help P3 it would need both an exact identity and an implementation
that constructs and uses it implicitly on the shared expression, with
that work charged. The identities tested here fail before that cost
obligation arises. Their failure does not show that another exact
shrinking-index recursion or a low-cost bulk jump is impossible.
