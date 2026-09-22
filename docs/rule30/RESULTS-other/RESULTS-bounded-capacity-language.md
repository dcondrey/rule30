# Small two-step capacity has an exact regular language

> **2026-09-13 continuation:** the previously capped family below is now
> closed, and the language classification extends through capacity 17.
> [The new uniform theorem](RESULTS-capacity17-mortality.md) proves sharp
> bounds N<=24 and D<=14 at every original length with Q_2<=17. The text
> below preserves the earlier computation and its explicitly incomplete cap.

**New all-length result:** every complete two-step original ancestor fiber of
size at most eight belongs to the explicit six-language classification below.
This reduces that entire capacity range to three spatially periodic families
and two exceptional second images. One family has a uniform mortality proof;
another remains unresolved even though its complete two-step fiber has only
six originals.

The unresolved family supplies an exact stronger obstruction to the proposed
two-step counting route: six original ancestors can share a successful tape
with twelve scalar repeats. This does not refute either unrestricted counting
conjecture, or every positive-rate estimate with an additive constant.
Period-two exclusion remains open.

All originals are legal auxiliary Z states. Every count below keeps the
original length fixed and retains the first two chronological guards. No
frontier is asserted to arise from the singleton seed.

## 1. A precise weaker alternative to an exponential bound

For an original w surviving two updates, write

```text
Q_2(w) = |E_2(r, first two scalars of w, Z^2(w))|.
```

Here E_2 is the complete original fiber from the
[canonical-ancestor report](RESULTS-canonical-merger-capacity.md). Consider the
following **unproved** qualitative hypothesis:

> For each integer K there is a finite B(K) such that every successful tape
> from every original with Q_2(w)<=K has at most B(K) repeats.

There is no required logarithmic growth, constant rate, or explicit formula
for B. This would suffice for mortality: each individual original has a finite
Q_2, so its D would be bounded, and the proved inequality

```text
r + N + 1 <= 2^(D+1)(r+2)
```

would bound its lifetime. A uniform positive-rate two-step fiber bound is a
stronger special case. Conversely, mortality alone does not automatically
give the displayed hypothesis: K is fixed while original length is unbounded.
An infinite family of individually mortal originals with fixed Q_2 and
unbounded D would refute this route without refuting mortality.

The useful new feature is that a fixed capacity range has an exactly
constructible regular language. Its spatial structure can be classified before
attempting temporal estimates. Spatial periodicity alone does not prove the
required temporal estimate.

## 2. Exact capped counting is a finite automaton

After an original prefix, let its first two bulk scans have column

```text
(p,u,v,U,V),
```

where p is the last original high bit, (u,v) the first scan's last output,
and (U,V) the second scan's last output. Upon reading x=2a+b,

```text
v' = v XOR (p OR b),       u' = u XOR (v' OR a),
V' = V XOR (u OR v'),      U' = U XOR (V' OR u').
```

The second bulk output y=2U'+V' fixes the upper pair. It is therefore enough
to retain eight nonnegative path counts indexed by (p,u,v), together with the
current (U,V). Each next output updates these counts by the nonnegative
integer matrix of compatible original symbols.

Fix K and replace every count n by min(n,K+1) after every update. This is
exact for deciding whether a final count is positive and at most K:
nonnegative addition and multiplication commute with this saturation, and
no discarded excess can later subtract from a count. The resulting machine
has at most `4*(K+2)^8` noninitial states. The legal origin has two initial
possibilities, 2 and 3; each gives precisely one initial inverse path.

At the end, the first guard with scalar s_0 selects the counts with
u=v=s_0. Scanning its birth symbol 3-s_0 in the second row changes
(U,V) to (U XOR 1,V XOR 1). Thus the second guard requires U=V, and its
scalar is s_1=1-U. The two symbols appended beyond the second bulk word are

```text
3*s_1, 3-s_1.
```

Summing the two selected counts, for p=0,1, therefore gives the exact guarded
E_2 cardinality whenever it is at most K. This is an automaton over **second
bulk output words**, with first and second scalar labels at acceptance.
The original language is its pullback through the actual two-layer scan;
the endpoint language is obtained by appending the displayed two symbols.
Neither operation introduces arbitrary current predecessors.

## 3. Complete classification through capacity eight

For K=8 the entire reachable capped-count graph has 47 states and 99 edges.
A separate closed product comparison verifies the following table as an
equality of regular languages, including their scalar and count labels.
This certifies **every original length**, rather than lengths below a cutoff.

| Second bulk output | First two scalars | Exact E_2 size |
|---|---|---:|
| `3` | `10` | 1 |
| `213(13)^k`, k>=0 | `00` | 6 |
| `303` | `00` | 2 |
| `30313(13)^k`, k>=0 | `00` | 6 |
| `21213(13)^k`, k>=0 | `00` | 6 |
| `21210` | `01` | 6 |

Append `03` in the first five rows and `32` in the final row to obtain the
full second image. These are all nonempty fibers of size at most eight;
in particular there are no fibers of sizes 3,4,5,7,8.

This classification supplies a substantive first case of the bounded-capacity
program. It does not claim the same form for arbitrary K. The free repetition
parameter k remains a real temporal obstacle.

## 4. Six ancestors can support twelve repeats

For every k>=0, set

```text
w_k = 20001 0^(2k),       r = 2k+5.
```

Its first two scalars are `00`, and its second image is

```text
Z^2(w_k) = 21213 (13)^k 03.
```

The complete original E_2 fiber is exactly

```text
{20001, 20020, 20021, 21001, 21020, 21021} 0^(2k).
```

**All-k proof.** Each of the six five-symbol prefixes emits second bulk
output `21213` and ends at column `(0,0,0,1,1)`. Reading `00` emits second
output `13` and returns to that same full column. Thus each displayed
original passes both guards and has the asserted common endpoint. The
complete classification proves there are exactly six inverse paths, so the
displayed originals exhaust the fiber for every k.

At k=30500, the representative has the exact complete successful tape

```text
original = 20001 0^61000,       r = 61005,
alpha = 001000001101001100000,
N = 21,       D = 12,          Q_2 = 6,
```

and its next guard fails. All six originals are independently replayed through
their first two guards and checked to have the same endpoint. The complete
representative trajectory, including failure, agrees between the maintained
engine and frozen `panel/cert33.py`.

Consequently a bound `Q_2 >= 2^(epsilon*D)` requires

```text
epsilon <= log_2(6)/12 = approximately 0.215414.
```

For `Q_2 >= 2^(epsilon*D-A)`, this witness only requires
`A >= 12*epsilon-log_2(6)`. It does not exclude all positive epsilon with
arbitrary fixed A. In the qualitative formulation, it proves B(6)>=12
if such a B exists. The complete unrestricted C_r(alpha) can be much larger
than these six ancestors because originals in other second images may merge
later. No conclusion about its upper or lower conjectured count follows.

## 5. One periodic-block family closes; the other has a recorded cap

For all k>=0, the second-image family

```text
z_k = 303 (13)^k 03
```

survives at most fifteen further updates. Including the initial `00`, its
originals therefore satisfy the sharp bounds N<=17 and D<=9.

The proof closes the complete spatial column orbit generated by the input
block `13` at each temporal depth through sixteen. Its largest period is
2048 blocks. Reading the final `03` and testing the complete guarded tape
signature leaves no accepted residue at depth sixteen. Every nonnegative k
is represented by a residue of each exact closed orbit. The full column
return proves spatial periodicity by determinism; no extrapolation from
sampled k is used. Independent frozen bulk scans check two complete copies
of every orbit. The lifetime and repeat maxima are both attained at k=2026,
whose total tape is `00100111100000101`.

For the other family `21213(13)^k03`, the analogous computation closes
spatial cycles through nineteen further updates. At depth nineteen the exact
period is 262144 blocks, and two residue classes survive. The next orbit
does not return within the declared 262144-block cap. Its closure is
**incomplete**, and the artifact explicitly records that fact. The exact
k=30500 witness above is mortal; it supplies no conclusion for all k.

This is where the small-capacity route currently stops. The difficult
family already has only six originals, so more detail about their two-step
connectivity cannot address its future repeats. A proof must constrain those
future guards, allow later merger capacity, or refute the qualitative
small-capacity hypothesis using this or another family.

## 6. Exact verification and scope

Run from the project root:

```text
uv run --no-project python experiments/rule30/bounded_capacity_language.py
```

The [verifier](../../experiments/rule30/bounded_capacity_language.py) and
[artifact](../../experiments/rule30/bounded-capacity-language.json) retain the
complete capped graph, the independent regular-language comparison, exact
original prefixes, temporal spatial-cycle residues and hashes, the explicit
unfinished cap, the six-ancestor witness and source hashes. The default has a
30-second wall cap and completed in under five seconds in the saved run.

The original-start census was not rerun. No paid compute, GPU, source oracle
change, or unrestricted enumeration was used. The all-length language theorem
and completed family certificate are proofs; the unresolved family's finite
residues and witness do not prove unrestricted mortality or period exclusion.
