# Weighted original histories: eight repeats with no loss of ancestors

Date: 2026-09-11. **The unrestricted bound with c=1 and epsilon=3/2 is
false. The proposed one-bit bound remains open.** An exact length-24 family
has 55,885,140 original ancestors, 15 repeats, and eight repeat edges during
which its entire original ancestor set is unchanged. A new weighted endpoint
identity counts this family without enumerating its original frontiers.
An all-length corollary of the existing reconstruction theorem also proves
that **every** ancestor class stops filtering after r successful updates:
each further prescribed continuation retains the whole class or kills it.

All states below are legal auxiliary reconstruction states. No singleton-seed
reachability is asserted. Original length stays fixed, and every chronological
guard is imposed. These results do not establish mortality, the period-two
exclusion, arbitrary center periods, or P2.

## 1. Exact counterexample to the stronger rate

Let

\[
 r=24,\qquad \alpha=00011100001111111100
                  =0^3 1^3 0^4 1^8 0^2.
\]

The exact count is

\[
 |C_{24}(\alpha)|=55\,885\,140,\qquad D(\alpha)=15.       \tag{1}
\]

There are \(2^{47}\) legal original words. Clearing the square root, the
claimed estimate with c=1 and epsilon=3/2 would require
\(|C|^2 8^D\le 2^{94}\). Instead,

\[
 \frac{55\,885\,140^2\,8^{15}}{2^{94}}
 =\frac{195196804551225}{35184372088832}>1.                \tag{2}
\]

This refutes an **unrestricted extension** of the stronger rate certified in
the [bounded-tape transfer report](RESULTS-cumulative-history-transfer.md).
That report's theorem for tapes of length at most nine remains valid.

The active one-bit inequality passes on this family:

\[
 \frac{55\,885\,140\,2^{15}}{2^{47}}
 =\frac{13971285}{1073741824}<1.                         \tag{3}
\]

Any unrestricted exponent with prefactor c=1 must therefore satisfy

\[
 \epsilon\le\frac{47-\log_2(55\,885\,140)}{15}
             =1.4176025745\ldots.                       \tag{4}
\]

Equivalently, a c=1 repeat base cannot exceed
\((2^{47}/55\,885\,140)^{1/15}=2.6714121499\ldots\).
Neither number is claimed sharp. A fixed prefactor c>1 can absorb a finite
counterexample, so (2) does **not** rule out epsilon=3/2 with some larger c,
or any positive-rate bound with unrestricted fixed c.

A second independently checked counterexample is

| Original length | Tape | D | Exact ancestors | Squared epsilon=3/2 ratio |
|---:|:---|---:|---:|:---|
| 22 | `00011111111111000` | 14 | 4,919,292 | `1512464611329/1099511627776 > 1` |
| 24 | `00011100001111111100` | 15 | 55,885,140 | `195196804551225/35184372088832 > 1` |

## 2. Eight repeats while the whole original set stays fixed

For the length-24 tape above, the prefix counts are

| Prefix | Exact original ancestors |
|:---|---:|
| `000111000` | 380,628,720 |
| `0001110000` | 62,426,052 |
| `00011100001` | 55,885,140 |
| Every subsequent prefix through `00011100001111111100` | 55,885,140 |

These are equality statements about **entire sets**, not just matching
cardinalities of unrelated fibers. The sets are nested under chronological
extension and are finite. Equal cardinality therefore implies equal sets.

The first plateau prefix has seven repeats. Extending it by seven more ones,
then two zeros, adds eight repeats without removing a single original ancestor.
This strengthens the previous three-repeat example at length six. It does
not prove arbitrarily long plateaus.

After the first nine updates, the contributing family has one endpoint:

```text
321021321030322121310303203030303
```

It emits `0`, then eight `1`s, then two `0`s, and its next update fails.
All 55,885,140 originals reach that endpoint with the same nine-symbol history
`000111000`. One concrete original is

```text
310333131311233123331121
```

The artifact gives its independently checked ancestry, the complete endpoint
itinerary, and every competing endpoint after the nine-symbol prefix. In
particular, successful continuation of the displayed endpoint is not being
used as a substitute for proving its original ancestry.

## 3. No further filtering after r successful updates

The [sector-assisted reconstruction](RESULTS-alt-trace-fiber.md) and the
explicit depth thresholds in the
[composition report](RESULTS-variable-length-episode-composition.md), section 5,
give the following uniform consequence for the counting problem.

**Synchronization theorem.** Fix an original length r>=1.

1. After r-1 successful updates, a prescribed tape and the original sector
   bit determine the endpoint. In particular, there are at most two endpoints.
2. After r successful updates, the prescribed tape alone determines the
   endpoint, including its sector.
3. Consequently, for every tape alpha with |alpha|>=r and every finite beta,

   \[
    \boxed{C_r(\alpha\beta)\in\{\varnothing,C_r(\alpha)\}.} \tag{5}
   \]

The statement includes empty ancestor classes. It assumes no mortality theorem.

**Proof.** For every successful image, the origin is `(1,sector)`, and the
second low bit satisfies

\[
 b_1=1\mathbin\oplus\mathrm{sector}.                    \tag{6}
\]

Indeed the scan starts with `v_0=sector`, and the next input's preceding high
bit is one. The length-one successful input, whose second output cell is the
appended cell, satisfies (6) directly.

At n=r-1>=1 the state length is 2n+1. Reconstruction fixes all highs at
indices at least one and all lows at indices at least two. The sector and
(6) provide the three missing coordinates, proving item 1. At r=1, item 1
just says the sector determines the legal one-symbol original.

At n=r the state length is 2r. The reconstructed terminal 2r-1 symbols now
include the entire state except the origin. In particular they include b_1,
so (6) determines the sector, proving item 2. Determinism then makes every
original in the class follow exactly the same future. Either the whole class
realizes a prescribed continuation or none does, proving item 3.

The threshold r cannot uniformly be replaced by r-1: the existing exact
class C_3(`00`) has six originals at endpoint `21303` and two at `30303`.
Thus the two sectors have not synchronized after r-1=2 emissions.

This is a corollary of the established reconstruction, not a separate claim
to a new reconstruction theorem. It substantially strengthens the obstruction
to a conditional contraction argument. After r successes, **all** later
successful repeats carry zero additional information about which original
ancestor was chosen. Any valid cumulative inequality must have already
acquired enough information to pay for all of them. The theorem does not
bound how many such future repeats there can be.

## 4. A general exact identity for weighted endpoints

This section is an all-length counting identity, rather than an inequality
inferred from the two witnesses. Fix temporal depth n>=1 and original length
r>=n, and put m=r-n+1. Let B denote the total input-length bulk scan, without
its guard or appended symbol. Use the column graph T_n and complete accepting
signature from the [transfer report](RESULTS-cumulative-history-transfer.md),
sections 2–3.

At the end of an original prefix record

\[
 q=(A_0,A_1,B_1,\ldots,A_n,B_n),
\]

where j denotes the j-th bulk iterate. Define

\[
 G_m(q,y)=\#\{\text{legal original m-prefixes with column q
                       and complete }B^n\text{ output }y\}.
\]

The output word y has length m. For each next original symbol x, write
\(q'=\delta_n(q,x)\). The exact recursion is

\[
 G_{m+1}(q',\,y(2A'_n+B'_n))\mathrel{+}=G_m(q,y),         \tag{7}
\]

starting from the two legal first symbols. Contributions are counted with
multiplicity even when their column states or output words coincide. Thus
\(\sum_{q,y}G_m(q,y)=2\cdot4^{m-1}\). A truncated prefix has no full frontier
guard: no local guard is imposed in (7).

For a prescribed n-symbol tape gamma, define

\[
 h_\gamma(q)=\#\{\text{original tails of length n-1 taking q
                         to Accept}(\gamma)\}.
\]

This is an ordinary backward path count on T_n, preserving labeled-edge
multiplicity. The accepting signature imposes **all n chronological guards**
of the completed original length-r frontier.

The last 2n-1 symbols after n successful updates are determined by gamma.
Call this word \(\eta_\gamma\). This is the established history reconstruction:
the low fields through inward depth 2n-2 and high fields through depth 2n-1
are already fixed by n emissions. Only depths through 2n-2 are used here.
Since the final length is r+n, the remaining prefix has length m and is
exactly y by autonomy of B on prefixes.

**Weighted endpoint theorem.** The number of original legal length-r words
that emit gamma and arrive at the full endpoint \(y\eta_\gamma\) is exactly

\[
 \boxed{E_{r,\gamma}(y\eta_\gamma)
            =\sum_q G_m(q,y)h_\gamma(q).}                \tag{8}
\]

**Proof.** Split an original word uniquely into its first m symbols and
remaining n-1 symbols. Formula (7) counts each prefix in exactly one class.
The column state is sufficient to extend the n bulk scans over any original
tail. A tail is admitted precisely when its completed column passes the
full-history signature, which is necessary and sufficient for every guard.
There are exactly h_gamma(q) such tails for every prefix in the class.
History reconstruction fixes the terminal 2n-1 cells, and prefix autonomy
fixes the other m cells to y. Multiplication followed by summation therefore
counts every original once. This proves (8).

For any continuation beta, applying the actual partial Z map to these weighted
endpoints gives

\[
 |C_r(\gamma\beta)|
   =\sum_{w:\,w\text{ successfully emits }\beta}E_{r,\gamma}(w). \tag{9}
\]

Each weight always counts the same original length-r words. No fresh frontier,
completion, or episode onset replaces their history.

For the length-24 witness, n=9 and m=16. Just 56,814 weighted records represent
all \(2^{31}\) original prefixes of length 16. Joining the remaining eight
original symbols counts the full universe of \(2^{47}\) original words.
Fourteen endpoints remain after `000111000`; continuing all fourteen gives
the prefix counts in section 2. At r=22 the analogous calculation has 16,952
prefix records and five endpoints after its prescribed nine-symbol prefix.

## 5. Exact verifier and independent check

Maintained files:

- [weighted_history_endpoints.py](../../experiments/rule30/weighted_history_endpoints.py)
- [weighted-history-endpoints.json](../../experiments/rule30/weighted-history-endpoints.json)

Run from the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 experiments/rule30/weighted_history_endpoints.py
```

The main engine implements (7)–(9), checks prefix mass exactly, retains every
endpoint, and compares every attempted future update with the unchanged
`panel/cert33.py`. Counts and inequality comparisons use integers.

A separate engine counts the two selected endpoint families directly from
original words using weighted column classes. For each class it keeps an
original-prefix representative. To extend it by one symbol, it recomputes all
n entire bulk scans using the frozen oracle and checks the prescribed endpoint
output prefix. It does not call the main transition graph, origin constructor,
or signature constructor. Column sufficiency, proved in the transfer report,
justifies grouping originals that have the same column and output prefix.

At the final original length, this independent engine replays each remaining
class representative with the frozen oracle, imposing the actual successful
tape and full endpoint. All members of a class have the same guarded outcome:
they share their terminal column and complete bulk output prefix. The weighted
sum is the exact endpoint ancestor count.

For r=24 this check recomputes 7,464 original-prefix edges, with at most 212
simultaneous column classes. It independently obtains 55,885,140 ancestors
and the concrete original above. The r=22 check recomputes 5,196 edges and
independently obtains 4,919,292. This is an exact compressed count, **not** a
claim to have individually replayed all 60,804,432 original words.

Additional controls check the newly stated synchronization consequences on
all 2,730 original words of lengths 1–6 using the frozen oracle, including the
two-endpoint example at r-1. This small check validates the new reconstruction
function and class-equality assertions; it does not rerun the earlier census
through length 12 or supply the all-length proof.
Only four nonempty one-symbol extensions in this small control reach the
synchronized regime; the uniform theorem rests on the depth argument above.

The saved run completed locally in under one second. The verifier has a
100,000-record cap, a 60-second time cap, and an 80-update continuation cap;
hitting a cap raises an error rather than producing a completed result. The
artifact records source hashes, endpoint weights, all target-prefix counts,
independent class counts, and explicit successful trajectories.

## 6. Remaining mathematical issue

The new endpoint identity keeps the full cumulative information and makes
large original fibers exactly countable. It supplies no inequality bounding
their weight in terms of all subsequent repeats. In the length-24 example,
the information acquired by the plateau onset must pay for eight later repeats.

The one-bit candidate, and the more flexible c>0, epsilon>0 information
bound, remain unproved and unrefuted. The successful finite witnesses and the
general counting identity do not close that gap.

**Follow-up, 2026-09-11.** The
[visible-low-bit investigation](RESULTS-constant-high-history-family.md) proves
an exact erasure formula for every fixed original high row. It certifies N<=16,
D<=8 for all original lengths when only the first low bit can affect the first
update, and proves a sharp conditional epsilon=1/8 information bound on that
base case. The [subsequent sparse-high obstruction](RESULTS-sparse-high-history-obstruction.md)
refutes this conditional epsilon=1/8 bound with two visible bits: conditional
probability 1/4 accompanies 18 repeats. The base case remains valid. Fixing the
opposite row does not justify a one-bit charge: 1664 directly verified members
of the length-24 family share one low row and exceed that conditional bound by
a factor 13/2. These are conditional-row statements, not counterexamples to
the unrestricted candidate.

**Original-variable continuation, 2026-09-11.** The
[guarded BDD investigation](RESULTS-guarded-history-bdd.md) counts complete
continuation trees directly over the same original variables. It independently
reproduces all endpoint-weighted counts in the length-22 and length-24 trees
and completes five additional selected trees. New exact full-history counts
at r=32 and r=35 have separate frozen-oracle endpoint-fiber checks. None
improves the exponent obstruction above or proves a uniform repeat charge.

**Encoding obstruction, 2026-09-11.** The
[original-coordinate analysis](RESULTS-history-encoding-obstruction.md) shows
that this same length-24 class cannot be encoded by retaining only 32 chosen
original coordinates: at least 39 are mandatory. Its affine hull has dimension
at least 41, allowing at most six independent affine restrictions on the
47 original bits. Both statements follow from 59 explicitly replayed originals.
The count (1) and the one-bit comparison (3) remain valid; the new result
excludes two representations of the required information rather than
refuting the information bound.
