# Split-value encoders: an obstruction and a valid three-update construction

**Status.** The assertion that every survivor belongs to a dimension-D_11
original-high-coordinate cube is false, including on the stated r=87
testbed. A masked toggle of a later
born terminal high has no successful predecessor. The proposed chronological
multi-repeat crash decoder has not been constructed. Neither general
split-value counting inequality is proved or refuted by these results.
Finite-frontier mortality and period-two exclusion remain open.

There is also a positive result: a coordinated four-symbol original rewrite
gives an injective family of `6*4^20` ancestors of the r=87 tape. The guards
are preserved and the words merge after three updates. This is a real
original encoding, with a block count rather than an unproved count of
independent repeat coordinates.

All originals are auxiliary legal frontiers. No singleton-seed ancestry is
asserted. Original length and every chronological guard are retained.

## 1. The final algebra is conditional on two missing inequalities

For a nonempty complete original history class, put

```
M = 2^(2r-1),  G = |C_r(alpha)|,
H = log2(G),   I = log2(M/G).
```

The identity H+I=2r-1 is exact. If I>=D_00 and H>=D_11 were proved for every
r and alpha, their sum would give the required repeat bound. That
conditional implication is correct. The local terminal-bit calculation does
not prove the two cumulative inequalities.

Also, W_r does not partition into C_r(alpha) and only crashed trajectories.
Its complement includes originals that emit another successful tape. For
example, at r=3 and a one-update horizon, `201` successfully emits 0 while
`333` successfully emits 1. For alpha=`0`, the latter lies outside C but
does not crash. I is the logarithmic fraction of originals excluded by the
prescribed history; it is not the logarithm of the crash-set cardinality.

## 2. A born terminal high cannot supply another chronological ancestor

**All-length obstruction.** Every successful Z-image ends in `3-s`, hence
in `2` or `3`. Its terminal high bit is therefore one. Toggling that high
produces a state ending in `0` or `1`. Such a state has no successful
one-step predecessor at any original length.

The scalar-one identity remains true for this modified current state:
when the terminal v is one, the last u update masks its input high. But
equal next images in the ambient legal universe do not imply equal
availability of chronological original ancestors. The original current
state is reconstructed by a successful trajectory; its toggled partner is
outside the successful-image language altogether.

For alpha=`001001111`, the `11` repeats are updates 7, 8, and 9. Each input
ends in the previous birth `2`. The proposed toggle is `2 -> 0`. It
preserves the next full image, but its modified input has no successful
predecessor. Thus it creates no additional original ancestor.

The `00` repeats at updates 2 and 5 give the analogous ancestry issue:
their input birth `3` becomes `1`. The modified guard fails, but this is
not a perturbation of a valid original trajectory up to that time.

## 3. The original-high hypercube fails at the testbed itself

The complete guarded two-step fiber at

```
r = 87,       first two scalars = 00,
Z^2(w) = 303 (13)^42 03
```

is exactly

```
{3011, 3030, 3031, 3111, 3130, 3131} 0^83.
```

The inverse-path verifier counts all original two-layer columns and then
imposes both terminal guards. It obtains exactly six words, independently
replayed through the complete tape prefix `001001111`.

Choose the particular member

```
w = 303 0^84.
```

It has D_11=3. However, **none of its 86 admissible single original high-bit
toggles even retains its first scalar 0**. With zero-based original indices:

| Toggled original high index | First update | Number |
|---|---|---:|
| 4,6,...,84 | Succeeds with scalar 1 | 41 |
| All other indices 1,...,86 | Guard fails | 45 |

Consequently the largest original-high-coordinate cube through w in
C_87(`001001111`) has dimension zero. A positive-dimensional coordinate
cube through w would require at least one valid single-coordinate neighbor.
This refutes the assertion that every survivor lies in a dimension-D_11
cube formed by toggling original high bits. It does not refute a lower
bound obtained by other encodings.

### Direct algebra behind the obstruction

The same first-scalar isolation holds for every word `303 0^(2k)`, k>=1,
of length r=2k+3. Its first four bulk outputs are `3210`, after which the
scan is at zero memory. Its first guard succeeds with scalar 0.

Toggling original high 1 leaves terminal pair (1,0); toggling high 2 leaves
(0,1). For any flipped index i>=3, the memory immediately after that
symbol is `(u,v,previous_a)=(1,0,1)`. If it is terminal, the guard fails.
Otherwise the next zero changes the memory to `(0,1,0)`. Each subsequent
zero toggles u and retains v=1, since

```
(u,v,0) --input 0--> (u XOR v,v,0).
```

Thus an interior even i succeeds with scalar 1 and an odd i fails. None
gives scalar 0. At k=42 this is exactly the table above. The verifier checks
the local zero-memory identity and independently replays all 86 testbed
perturbations; the all-k statement follows from the parity calculation.

## 4. What the first-step crash toggle does establish

For any original class beginning with scalar 0, toggling the original
terminal high changes the first terminal pair from (0,0) to (1,0), producing
a failed first guard. Original legality is preserved because such a
nonempty class has r>=2. The failed output's terminal u recovers the one
payload bit, and toggling back recovers the original.

On the displayed six-member subset this gives exactly twelve distinct
original outputs: six originals and six first-step crashes. All are
independently checked.

This is a one-bit encoder associated with the first scan. It is not a
two-bit encoder indexed by the two `00` repeats. A branch that has already
failed has no further actual partial-Z updates. A multi-bit decoder could
in principle recover more information from a suitably constructed original
or failure state, but its operations, injectivity, and decoding would have
to be specified and proved. No impossibility of every such encoder is
asserted here.

## 5. A valid coordinated original encoding merges at update three

Set

```
P in {3011,3030,3031,3111,3130,3131},
B in {0000,0101,0120,0121}.
```

After any P, the three consecutive bulk scans have terminal memories

```
(0,0,0), (0,1,0), (0,0,0),
```

and their four-symbol outputs are `3210`, `3031`, `3210` respectively.
Each allowed B preserves all three incoming memories, with the following
bulk outputs:

| Original block | First bulk block | Second bulk block | Third bulk block |
|---|---|---|---|
| `0000` | `0000` | `3131` | `3210` |
| `0101` | `0310` | `3031` | `3210` |
| `0120` | `0310` | `3031` | `3210` |
| `0121` | `0310` | `3031` | `3210` |

**Original product theorem.** Fix m>=0 and any common finite suffix S.
The `6*4^m` distinct legal originals

```
P B_1 ... B_m S
```

have the same successful chronological scalar tape as `3011 0^(4m) S`.
On three successes, their full third images coincide.

**Proof.** The block exits equal their entrances in all three rows, so
arbitrary concatenations preserve the three terminal memories and the third
bulk output. The common suffix scans from the same memories. Equal first
terminal memory gives the same first guard and birth. In row two, identical
boundary memory scans that identical birth, giving the same second guard
and birth. Row three likewise scans an identical appended two-symbol
suffix. Thus all actual guards and scalars agree; any earlier failure is
simultaneous. On three successes, the entire third image agrees, after which
determinism preserves every subsequent update. The prefix and fixed-length
blocks occupy disjoint positions, so their choices decode uniquely. This
proves injectivity and the count.

For m=20 and S=`000`, all words have length 87 and emit `001001111`, giving

```
|C_87(001001111)| >= 6*4^20 = 6,597,069,766,656.
```

The simple extras `3011 B 0^79`, for B=`0101`,`0120`,`0121`, lie outside
the original six-member second-image fiber and first merge with it at
update three. Their complete nine-update trajectories are independently
replayed. The product result comes from the local induction, not enumerating
its trillions of originals.

The construction also gives an explicit distribution among second images.
At each block, choice `0000` emits second bulk block `3131`; each of the
other three choices emits `3031`. These distinct equal-length output blocks
recover the zero/nonzero choice pattern uniquely. Thus, on three successes,
there are exactly `2^m` second images **within the constructed family**. A
pattern with j nonzero blocks contains exactly `6*3^j` constructed originals.
Their total weight is

```
sum_(j=0)^m binomial(m,j)*6*3^j = 6*4^m.
```

All those second-image components merge at update three. For m=20 this is
`2^20` distinct second images. These are exact weights within the constructed
subfamily, not asserted complete Q_2 counts for each component. The three
`11` repeats at updates 7,8,9 occur after all constructed originals have
already coalesced; no additional merger among them occurs at those repeats.

There are nevertheless large original-high-coordinate cubes elsewhere in
this class. Fix P and S and choose each B independently from `0101` and
`0121`; these differ only in the high bit of their third symbol. At m=20
this gives a 20-dimensional original-high-coordinate cube. It lies in one
other second-image component, since both blocks have second output `3031`.
Thus the obstruction in section 3 is to a cube through **every** survivor,
not to the existence of any high-coordinate cube in the complete class.

This supplies actual global ancestors for the testbed, using coordinated
original edits. It does not prove that an arbitrary tape contains enough
such blocks in terms of D_11 or D.

## 6. Exact merger accounting and its remaining obligation

For the prescribed prefix alpha_1...alpha_t, define m_t(x) to be the number
of original legal length-r words that pass every one of those guards and
end at x. Then exactly

```
m_(t+1)(z) = sum m_t(x) over x with Z(x)=(z,alpha_(t+1)).
```

The summands count disjoint original sets. A merger adds their weights.
The total G_t=sum_x m_t(x) decreases only when original sets fail the next
guard or emit another scalar; merging itself preserves their total weight.
This is bookkeeping for original ancestors, not a count of arbitrary new
predecessors at the current length.

At t=2 the weights are precisely the original guarded Q_2 values. For a
longer prescribed tape, its full C_r class is a disjoint union of those
whole Q_2 fibers whose endpoints have the required continuation. The
three-update construction gives an explicit example of this union being
much larger than one component.

This is a valid framework for tracking mergers, but it supplies no
cumulative repeat inequality by itself. In particular, after r successes
the proved [synchronization theorem](RESULTS-weighted-history-endpoints.md)
leaves at most one endpoint. Its original weight stays constant along every
successful continuation. Any merger-based argument must account for later
repeats after this point as well.

The [temporal operator audit](RESULTS-temporal-operator-audit.md) makes that
formulation explicit. Synchronization does not stop length growth; exact
temporal transitions map length-L frontiers to length-(L+1) frontiers.

For the particular nine-symbol testbed, both split inequalities can be
certified by valid existing and new arguments. The
[bounded-tape upper theorem](RESULTS-cumulative-history-transfer.md) already
gives I>=D=5 because the tape has length nine. The construction above gives
H>=log2(6*4^20)>42, hence H>=D_11=3. This settles this individual instance,
not the uniform split conjecture or the proposed encoders.

## 7. Exact verification and scope

```
uv run --no-project python experiments/rule30/split_encoder_obstruction.py
uv run --no-project python experiments/rule30/three_update_block_family.py
```

Files:

- [Encoder obstruction verifier](../../experiments/rule30/split_encoder_obstruction.py)
- [Encoder obstruction artifact](../../experiments/rule30/split-encoder-obstruction.json)
- [Three-update construction verifier](../../experiments/rule30/three_update_block_family.py)
- [Three-update construction artifact](../../experiments/rule30/three-update-block-family.json)

The obstruction verifier recovers all six originals, checks all 86 admissible
single-high perturbations, verifies the born-terminal modifications and
twelve first-step encoding outputs, and records 153 attempted updates
checked against frozen `panel/cert33.py`. It has a 30-second wall cap.

The construction verifier checks all 256 local four-symbol blocks, checks
30 bulk scans with the frozen oracle, and independently checks 90 actual
guarded updates on the baseline, extra ancestors, and mixed block controls.
It has a 10-second wall cap. Both verifiers completed in under a second and
save source hashes and explicit scope flags. The old census and upper-bound
certificate were not regenerated. No GPU or paid compute was used, and
the frozen oracle was not changed.
