# Eventual-constant-tail separator after the first-infinite shift

Date: 2026-09-01

Status: **THE FIRST-INFINITE-TAIL REDUCTION LEAVES ONLY CUT TAILS `2^omega`
AND `3^omega`.  BOTH FIBERS ARE EXHAUSTIVELY SEPARATED THROUGH CUTOFF 23 AND
EVOLUTIONARILY STRESS-TESTED THROUGH CUTOFF 96.  AN EXACT SPATIAL-SHIFT MAP,
AN AFFINE THREE-BIT BOUNDARY COCYCLE, AND A SCALE-INVARIANT FINITE-WORD
REDUCTION ARE NOW AVAILABLE.  THE SCALE WORD IS SEPARATED THROUGH LENGTH 22,
AND THE STRONGER REVERSED-DIAGONAL QUEUE IS MORTAL THROUGH LENGTH 15, BUT NO
ALL-LENGTH INDUCTION HAS BEEN PROVED.  PERIOD-TWO MORTALITY AND P1 REMAIN
OPEN.**

The exact census is `eventual_constant_tail.py`.  The GA witnesses and their
independent replay live in `experiments/openevolve-p1-rank-zero/`.

## 1. Why these two tails suffice

Let `x^j=I(sigma^j e)`.  The rotated identity gives

```text
P(x^(j+1)) = sigma^2 x^j.                            (1)
```

If `x^0` is finite and the hard-core endpoint continued forever, not every
`x^j` could remain finite: while two consecutive cuts are finite, preservation
of the last nonzero coordinate under `P` makes their support endpoints differ
by exactly two.  At the first infinite `x^j`, equation (1) makes `P(x^j)`
finite.  Its tail therefore follows

```text
u_(t+1)=g_0(u_t),  g_0=(0,3,2,3).
```

The nonzero eventual orbits are exactly the fixed states `2` and `3`.  Hence a
uniform proof of

> no cut eventually equal to `2^omega` or `3^omega` has a hard-core terminal
> endpoint

would close the rank-zero separator, and therefore the full finite-Peel-rank
obstruction.

## 2. Exact triangular census

For a cutoff `T` and tail `c` in `{2,3}`, enumerate every hard-core endpoint
prefix of length `T`, reconstruct its unique cut prefix, append `c^omega`, and
apply the terminal cone.  This covers every member of the stated cutoff fiber;
there is no SAT model or free post-cutoff boundary.

The exact maximum hard-core prefix lengths through `T=23` are:

```text
T:       1  2  3  4  5  6  7  8  9 10 11 12
tail 2:  2  2  5  5  6  7 10 10 10 11 13 14
tail 3:  1  3  3  5  5 10 10 10 10 12 13 14

T:      13 14 15 16 17 18 19 20 21 22 23
tail 2: 16 18 19 19 19 20 22 24 24 26 28
tail 3: 15 18 18 19 26 26 26 26 26 26 29
```

Every value is below `2T+2`.  As in the zero-tail census, this is a finite
table and not an induction.

## 3. Evolutionary stress test

The bit-level GA was calibrated at `T=23`: it recovered the exact maxima `28`
for tail `2` and `29` for tail `3`.  Selected larger results are:

| cutoff `T` | tail `2` survival | tail `3` survival | `2T+2` |
|---:|---:|---:|---:|
| 32 | 42 | 37 | 66 |
| 48 | 56 | 56 | 98 |
| 64 | 74 | 72 | 130 |
| 96 | 103 | 110 | 194 |

No run reaches the proposed bound.  These are exact witnesses at the displayed
cutoffs, but the GA is neither exhaustive above `T=23` nor proof-producing.

## 4. Proof-bearing next target

The accepted endpoint language has the exact prefix grammar

```text
HC = 2 HC  union  12 HC,
I(qe) = (B(q), phi(q,I(e)_0)) . P(I(e)).              (2)
```

Equation (2) supplies the correct unbounded search grammar.  A useful evolved
object would be a recursive separator whose two branch rules are checked
symbolically for both tail modes `2` and `3`, carry the one-symbol boundary
annotation explicitly, and reduce a well-founded structural measure.  A
numerical score on more cutoffs is not a replacement for those branch checks.

`RESULTS-ENDPOINT-FLIP-COCYCLE.md` supplies the corresponding exact morphing
operator: changing endpoint defect `k` rewrites only cut interval
`[k,2k+1]`.  Thus the candidate measure must control ordered overlaps of those
intervals; raw support is not contracting because the rewrite frontier can
escape to infinity.

## 5. Exact partial shift on cut lassos

There is no nondeterminism after an eventually-periodic cut is fixed.  Put
`x=I(e)`, `y=I(sigma e)`, and `a_j=B(e_j)`.  The first two cut cells obey

```text
x_0=a_0,
x_1=phi(B(a_0),a_1).
```

On the hard-core domain `a_j in {1,2}` with no pair `22`, these equations
uniquely decode `a_1` whenever a valid next endpoint symbol exists.  The
rotated identity and right-permutivity then give all remaining cells:

```text
y_0=a_1,
y_(t+1)=g_(x_(t+2))(y_t).                            (3)
```

Thus endpoint shift is a deterministic partial map on canonical eventually
periodic cut lassos.  `constant_tail_shift.py` implements (3), checks it
against every hard-core endpoint word through length nine, and reproduces
every maximum in section 2 through cutoff 23.  No lasso orbit cycles in that
census.

The tail periods along the maximizing orbits are not bounded by four.  They
progress from periods `1` to `2`, `4`, and `8`; the abstract periodic-tail
chain first reaches period `16` after 200 endpoint shifts.  Consequently the
promising period-at-most-four pattern at small cutoff was a finite artifact.
The hard-core decoder prunes the abstract lift tree strongly, but it does not
make the periodic tail family finite.

## 6. Exact audit of the period-doubling profile

`constant_tail_doubling.py` records the cycle word immediately before and
after every period doubling.  On 5,172 exact hard-core lasso orbits (all
hard-core endpoint prefixes through cutoff 14, plus the recorded GA
witnesses), the profile

```text
(period, symbol counts, return transformation,
 half-period disagreements, half-period bit defect)
```

appears to form a deterministic six-node, six-edge graph.  That graph is a
finite-corpus pattern, not an induction.  The script now subjects it to a
strictly stronger cutoff-independent-in-endpoint test: it exhausts all 65,536
primitive four-symbol words of dyadic lengths `1,2,4,8`, all four states
entering their periodic tails, and all 1,112 lifts that double the period.
At the `8 -> 16` transition, four input profiles each have two different
output profiles.  Thus the five-component profile is **not** a closed
inductive state and the apparent six-state graph cannot prove mortality.
One literal collision certificate is

```text
driver cycles:  00000111              00001101
shared profile: (8,(5,3,0,0),(3,2,3,2),3,3)
lifted cycles:  2222223233333323      2222232233333233
return maps:    (0,0,0,0)             (2,2,2,2)
```

The two lifted cycles have otherwise identical displayed profiles.  In
particular, adding only period, symbol counts, and half-period defect data
cannot repair the collision.

There is one uniform positive fact behind the audit.  Exactly three elements
of the 13-element lift monoid have a two-cycle, and each has a unique
two-cycle.  Therefore, whenever a fixed driver cycle doubles, its lifted
cycle word is unique up to rotation: choosing the other cyclic entry state
only rotates the output by one driver period.  The exhaustive audit has zero
exact-cycle collisions, as this lemma requires.  What remains unbounded is
the exact cycle word itself; period-preserving shifts can change it before the
next doubling.  A proof must therefore find a recursive word-level invariant
or a sound finite quotient finer than the rejected profile.

Even the exact cycle word is not a deterministic state independent of the
lasso prefix.  Starting from each constant tail and allowing all four states
that a finite prefix could feed into the periodic tail, the canonical cycle
has a unique successor for 26,603 endpoint shifts.  Its periods change as

```text
tail 2: step 0:1, 2:2, 4:4, 15:8, 200:16
tail 3: step 0:1, 1:2, 4:4, 14:8, 200:16.
```

At shift 26,603 both prefix-independent cycle orbits branch:

```text
tail 2 driver 0000330003030033, return (0,2,2,2)
  -> 0000020000220002 or 0022202222202222

tail 3 driver 0000110001010011, return (2,3,2,3)
  -> 2222232222332223 or 2233323333323333.
```

Each displayed return map has two fixed points.  This is an exact negative
for a cycle-only deterministic recurrence: a proof must retain enough of the
finite lasso prefix to select the entry state.  It does not assert that both
branches are realized by hard-core endpoint prefixes.

## 7. Eight affine boundary permutations

Encode a four-state symbol by bits `(h,l)`.  Every permutation taking a newly
appended endpoint symbol to the newly exposed cut symbol has the affine form

```text
(h,l) -> (h + alpha, l + beta*h + gamma),
alpha,beta,gamma in F_2.                             (4)
```

All eight triples occur.  Composition is the explicit three-bit cocycle

```text
(a,b,g) after (A,B,G)
  = (a+A, b+B, g+G+b*A).                             (5)
```

The local left translations themselves have coordinates

```text
L_q = (activity(q), 1+low(q), activity(q)).          (6)
```

Both remaining constant tails have high bit one.  If the current boundary
permutation is `(alpha,beta,gamma)`, forcing a high-one cut symbol makes the
endpoint high bit `1+alpha`.  Hence the endpoint is state `2-alpha`; the
hard-core prohibition of endpoint `11` becomes the prohibition of consecutive
`alpha=1`.  The low cut bit supplies the second equation

```text
low(c) = alpha + beta*(1+alpha) + gamma.              (7)
```

Equations (4)-(7) are exact and reduce the D8 boundary action to two additive
coordinates plus one cocycle coordinate.  They do not yet close under endpoint
extension: the next affine triple still depends on an ordered, growing
diagonal of internal states.

## 8. Scale-block reduction

The dependency window of the inverse cut is

```text
I(e)_t depends only on e_(floor(t/2)),...,e_t.        (8)
```

Fix a word `W` of length `n`.  Pad it on the left by any `n` symbols and,
starting at endpoint coordinate `2n`, append the unique endpoint symbols that
force cut coordinates `2n,...,4n-1` to equal `c`.  By (8) the resulting
length-`2n` block is independent of the padding; call it `R_c(W)`.

If a hard-core endpoint had inverse cut eventually equal to `c`, then for
every sufficiently large `n`

```text
W=e_[n,2n)       and       R_c(W)=e_[2n,4n)          (9)
```

would both be hard-core.  Therefore the complete constant-tail separator is
reduced to the following scale-invariant finite-word lemma:

> For `c in {2,3}` and every nonempty hard-core word `W`, the forced block
> `R_c(W)` is not a hard-core continuation of `W`.

This is a genuine all-length lemma: proving it would finish both tail modes,
the rank-zero separator, and the nonconstant period-two exclusion.  It is
exhaustively true through `|W|=22`.  The maximum initial hard-core lengths in
`R_c(W)` are

```text
|W|:       1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22
tail 2:    0  1  1  2  1  2  4  3  2  4  4  5  5  7  7 10 10  9  7 10 12 10
tail 3:    1  1  4  2  2  2  4  3  8  6  4  5  5  5  6  6  5  9  8  8  8  9
```

Every recorded value is strictly below `2|W|`, as required.  This table is a
falsifier for the scale lemma, not its proof.  Its strategic advantage over
the cutoff table is that the statement has no moving pre-tail prefix or
external boundary mode: it is one word-to-word exclusion at every scale.

The first census through length 16 suggested a more specific charging lemma.
Let `s_c(W)` be the length of the initial hard-core continuation inside
`R_c(W)`.  Through length 16,

```text
s_2(W) <= number of state-2 symbols in W,
s_3(W) <= number of state-2 symbols in W + 3.         (10)
```

The tail-2 part of (10) is **false**.  Its first exact counterexample is

```text
|W|=17, W=12212121212121212,
s_2(W)=10, number of state-2 symbols=9.               (11)
```

The forced block starts `2122122121` and then creates `11`.  This is a
counterexample only to the proposed intermediate count, not to the scale
separator.

The contact in the initial `22` gives a smaller repaired target that survives
the complete census through length 22:

```text
s_2(W) <= #2(W) + indicator(22 occurs in W),
s_3(W) <= #2(W) + 3.                                  (12)
```

Both bounds would prove the scale lemma.  For tail 2 the right side is at
most `|W|+1<2|W|` for `|W|>=2`, with length one checked directly.  For tail 3
it is at most `|W|+3<2|W|` for `|W|>=4`, with the three smaller lengths checked
directly.  The first inequality is sharp at (11); the second is sharp at
`W=121`, length three.  Random, nonexhaustive controls at lengths 24, 32, 48,
and 64 also found no violation.  Exhaustive through length 30 as of
2026-09-16 (`seam_history_hc_charge.py`, `RESULTS-HC-COMPOSITION-CHARGE.md`):
no violation, minimum slack 4 to 11 at lengths 23 to 30, no further sharp
case after (11).

The exact incremental dependency diagonal

```text
d'_0=B(q),  d'_1=phi(e_last,d'_0),
d'_t=phi(d_(t-2),d'_(t-1))                            (13)
```

computes a forced scale block in quadratic rather than cubic time and was
cross-checked against the literal inverse cone in 41,868 cases.  It enabled
the length-22 census and is also a possible proof coordinate: (11) shows that
an ordered proof must allow one contact-created credit.  A naive deletion
induction on either end of the hard-core grammar still fails.  Equation (12)
is therefore a falsifier-backed target, not a proved charging argument.

## 9. Reversed-diagonal queue target

There is also an exact one-word form of the growing formula.  Let `D_m` be
the complete right-edge diagonal of the inverse-terminal triangle after `m`
endpoint symbols, and reverse it to `R`.  On a constant-tail step `R_0=c`.
Right-permutivity turns the next diagonal into the prefix scan

```text
S_0=c,   S_i=g_(S_(i-1))(R_i).
```

The final scan state uniquely decodes the next endpoint symbol, and the new
queue is `S` followed by its boundary encoding.  Hard-core legality is a
three-case condition on the old final symbol and the final scan state.

Consequently it is sufficient to prove that every finite word beginning in
`c in {2,3}` and ending in `{1,2}` is mortal under this deterministic partial
queue map.  This is stronger than the scale lemma because the middle of the
word is allowed to be an arbitrary four-symbol word, not merely an
endpoint-derived diagonal.  The scan has the exact quotient `3 -> 1` in every
nonleading input coordinate, reducing the arbitrary middle alphabet to
`{0,1,2}` without changing mortality or the emitted endpoint.  A complete
six-state DFA calculation further proves that every normalized successor
avoids `20`, `22`, and `011`, including across the appended hard-core
boundary.  The candidate bound `lifetime(R)<=|R|` is exact through length 15
over all such words.  This remains a finite census, but the operator,
quotient, invariant image language, and reduction are uniform.  See
`RESULTS-CONSTANT-TAIL-QUEUE.md` and `constant_tail_queue.py`.

## 10. Exact language morph and failed DFA-rank contraction

Let `L_h(c)` be the invariant normalized queues that survive at least `h`
more updates.  Sequential-transducer closure gives the exact formula update

```text
L_(h+1)(c)=L_0(c) intersect Q_c^(-1)(L_h(c)).
```

`constant_tail_language_cocycle.py` constructs this regular preimage and
minimizes it.  The minimized formula does not contract: for `h>=1` through
the checked horizon seven it has `4^(h+1)+1` states, while accepting states
have Fibonacci counts `5,8,13,...,89`.  Thus ordinary DFA rank is not the
well-founded quantity suggested by the dynamic-formula proposal.

The shortest accepted queue length is more useful.  For the two tail modes it
progresses from `1/2` to `3`, `5`, and `10`, with plateaus between jumps.
Proving that this minimum tends to infinity would prove mortality.  This is
the precise amortized language-cocycle target; see
`RESULTS-CONSTANT-TAIL-LANGUAGE-COCYCLE.md`.

## 11. Eventual actual-right refinement

The all-hard-core scale and queue lemmas are stronger than the period-two
application requires.  Let `e` be the endpoint supplied by a genuine
alternating-center counterexample, so state `1` encodes `rho=1`, state `2`
encodes `rho=0`, and the binary word underlying `e` is an actual right trace.
If `I(e)` has finite rank `m`, the rank descent replaces it by

```text
f = 2^m e.                                             (14)
```

At the first shift `j` whose inverse cut is infinite, the endpoint is either
`2^(m-j)e` or a shift of `e`.  In either case it has a tail equal to a tail of
the original actual right trace.  Its inverse cut is eventually constant 2
or 3 by the first-infinite-tail lemma.

Choose the scale `n` beyond both finite prefixes.  Then the entire endpoint
block

```text
f_[n,4n) = W R_c(W)                                   (15)
```

is a factor of a genuine alternating-center right trace.  Consequently the
period-two theorem needs only the following weaker separator:

> For `c in {2,3}`, no actual-right factor `W` has `R_c(W)` as an
> actual-right continuation.

This is a uniform logical reduction; it does not prove the separator.  It
also explains why actual-right restrictions cannot prove the stronger
abstract rank-zero separator for every hard-core endpoint, while remaining
available for the original period-two problem.

`constant_tail_right_filter.py` audits this intersection.  Its regular
prefilter uses every proved minimal forbidden right factor through length 11.
At scale 27 that relaxation still permits survival 7 for tail 2 and 9 for
tail 3.  Exact SAT membership in the complete finite right-light-cone
language lowers both maxima to 5.  Selected exact actual-right maxima are

```text
scale n:           10  15  20  24  27
tail 2 maximum:     4   4   4   4   5
tail 3 maximum:     5   3   4   5   5
```

These are finite results, not a universal constant-five theorem.  The
length-27 finite-factor extremizers with survivals 7 and 9 are both rejected
by the full right-light-cone SAT instance.  This demonstrates that the exact
right language contributes information not captured by the current finite
forbidden-factor list.

## 12. Reproduction

From `13-rule30/`:

```bash
uv run python experiments/rule30/p1-period2-invariant/eventual_constant_tail.py \
  --max-cutoff 23
uv run python experiments/rule30/p1-period2-invariant/constant_tail_shift.py \
  --max-cutoff 23
uv run python experiments/rule30/p1-period2-invariant/constant_tail_doubling.py \
  --max-exhaustive-cutoff 14 --universal-max-period 8 \
  --json experiments/rule30/p1-period2-invariant/constant-tail-doubling.json
uv run python experiments/rule30/p1-period2-invariant/constant_tail_scale.py \
  --max-scale 12
uv run python experiments/rule30/p1-period2-invariant/constant_tail_queue.py \
  --control-length 7 --max-queue-length 15 --orbit-cap 1000
uv run python \
  experiments/rule30/p1-period2-invariant/constant_tail_language_cocycle.py \
  --max-horizon 7
uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/constant_tail_queue_sat.py \
  --max-horizon 20 --max-length 40
uv run --project experiments/sygus-p3 python \
  experiments/rule30/p1-period2-invariant/constant_tail_right_filter.py \
  --max-scale 1 --actual-scales 10 15 20 24 27
uv run python experiments/openevolve-p1-rank-zero/verify_results.py
```

The recorded tail runs used population 96, 120 generations, and seeds 52000
and 53000 respectively:

```bash
uv run python experiments/openevolve-p1-rank-zero/ga_witness_search.py \
  --tail 2 --cutoffs 23 32 48 64 96 --population 96 --generations 120 \
  --seed 52000 --json experiments/openevolve-p1-rank-zero/ga_tail2_results.json
uv run python experiments/openevolve-p1-rank-zero/ga_witness_search.py \
  --tail 3 --cutoffs 23 32 48 64 96 --population 96 --generations 120 \
  --seed 53000 --json experiments/openevolve-p1-rank-zero/ga_tail3_results.json
```
