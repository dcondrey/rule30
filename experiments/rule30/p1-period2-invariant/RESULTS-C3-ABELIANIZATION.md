# C3 already holds in the abelianization: gamma is not needed

Date: 2026-09-07. Script: `c3_abelianization_probe.py`.

Status: **C3 SURVIVES THE QUOTIENT BY THE CENTRE. The 2-bit abelianization of
the newest-cut group carries C3 by itself, with zero failures on all 72,351
legal rows through length 21, clearing the length at which the pointwise-derivative
certificate died. Since the quotient map is a homomorphism, this is a STRICTLY
STRONGER statement than C3, and it identifies the proof target as two GF(2)-affine
functionals rather than an 8-element non-abelian group. The abelianization turns
out to be exactly the project's own `(alpha, beta)` coordinates; `gamma`, the
quadratic one, is the kernel and is never required.**

Evidence level: `R` for the implication (a homomorphism argument, given below,
independent of measurement); `K` for the census.

Provenance: this came out of auditing an outside proposal that located the
Rule-30-specific mechanism in the *non-commutativity* of the newest-cut group.
That proposal's algebra was wrong in five places (see
`RESULTS-C14-KILL-AND-RULE90-CONTROL.md` and the session log): it took
`L(0) = (0,1,3,2)` for an order-4 rotation when it is an involution, identified
the centre as `{id, BOUNDARY}` when BOUNDARY is not central, and rested on
`L(2)L(0)L(2) = L(0)^-1 != L(0)`, which is vacuous because `L(0)` is an
involution. Checking those errors is what raised the question this file answers,
and the answer runs against the proposal's thesis.

## 1. The group, correctly

Generators, as 4-tuples indexed by the incoming state:

```text
L(0) = (0,1,3,2)   order 2
L(1) = (3,2,1,0)   order 2      ( = BOUNDARY )
L(2) = (3,2,0,1)   order 4      <- the only order-4 generator
L(3) = L(1)                     ( the Phi(2,.) = Phi(3,.) collapse )
```

The generated group has order 8 with element orders `[1,2,2,2,2,2,4,4]`, so it
is D8. Verified facts that a proof may use:

- centre `Z = {id, (1,0,3,2)}`, and `(1,0,3,2) = L(2)^2`;
- commutator subgroup `[G,G] = Z`, so the abelianization is `G/Z ~ Z2 x Z2`;
- `BOUNDARY = L(1)` is **not** central;
- `L(1) o L(0) = L(2)` exactly.

## 2. The abelianization is `(alpha, beta)`

Let `phi: G -> G/Z ~ Z2 x Z2`. On generators, writing states as two bits:

```text
phi(L(s)) = ( activity(s), not lo(s) )   where activity(s) = hi(s) OR lo(s)
```

checked for all four `s`. That pair is exactly `(local_alpha, local_beta)` in
`newest_affine_bits`. So the project's existing affine coordinates decompose as

```text
(alpha, beta)  =  the abelianization G/Z          (linear over GF(2))
 gamma         =  the central coordinate          (the quadratic cocycle term,
                                                   carrying local_beta & old_alpha)
```

This is not a new coordinate system. It is a statement about the one already in
the code: `alpha` and `beta` are the abelian part, `gamma` is the kernel.

## 3. The claim and why it implies C3

Define the abelianized sensitivity set

```text
S_j^ab = { k : phi(A_(j,k)) != phi(A_(j,k+1)) }
```

> **C3ab.** For every nonempty hard-core `W`, tail `c in {2,3}`, and legal row
> `j`:  `max S_j^ab >= j`.

**C3ab implies C3.** `phi` is a homomorphism, so
`phi(A_(j,k)) != phi(A_(j,k+1))` forces `A_(j,k) != A_(j,k+1)`. Hence
`S_j^ab` is a subset of `S_j`, so `max S_j^ab <= max S_j`, and
`max S_j^ab >= j` gives `max S_j >= j`. With `C3 ==> (1)` already established,
`C3ab ==> C3 ==> (1)`. QED

Note the direction: **C3ab is stronger than C3, not weaker.** It is the usual
strengthening-to-make-the-induction-work move. It is worth adopting only because
it is true on the corpus and its object is two bits instead of eight group
elements.

## 4. Measurement

Exhaustive over hard-core words, both tails, legal rows only (tail 3's final row
exempt):

```text
through length 12:     964 legal rows,  C3 failures 0,  C3ab failures 0
through length 14:   2,386 legal rows,  C3 failures 0,  C3ab failures 0
through length 18:  16,507 legal rows,  C3 failures 0,  C3ab failures 0
```

The length-12 figure is from the committed script run with `--verify`, which
first checks the forcing against the frozen `zero_prefix_bitsliced_graph` on
every hard-core word to length 10 and then scores both claims. C3ab slack
(`max S_j^ab - j`) has minimum 0, attained on 2 rows — the same two tight rows
that make C3 tight, `W = 121` and `W = 221`, tail 3, row 2.

At length 18 the C3ab slack minimum is still 0 and still attained on exactly 2
rows, so the tight set has not grown with `n`: it remains `W = 121` and
`W = 221`, tail 3, row 2. Section 4d carries this to length 21. **Beyond
length 21 is unchecked.**

Distribution of the group element mediating each sensitivity event,
`A_(j,k)^-1 A_(j,k+1)`, over all sensitive tokens to length 14:

```text
(3,2,1,0) 3694    (2,3,0,1) 3434    (2,3,1,0) 3255    (1,0,2,3) 3126
(1,0,3,2) 2996  <- the central element, invisible to phi
(3,2,0,1) 2879    (0,1,3,2) 2556
```

So central differences are common — 2,996 events that `phi` cannot see — and
C3ab still holds. The non-central differences suffice on their own at every
legal row.

## 4a. Two bits exactly: neither coordinate suffices alone

Scoring C3 through each single coordinate of the abelianization, same corpus to
length 14, 2,386 legal rows:

```text
full group (8 elements)   failures  0
abelianization (2 bits)   failures  0
alpha alone (1 bit)       failures  4    first: W=21212122, tail 2, row 2,
                                          S_j^ab = {3,6,7} but S_j^alpha = {}
beta  alone (1 bit)       failures 14    first: W=22,       tail 2, row 0,
                                          S_j^ab = {1}     but S_j^beta  = {}
```

So the abelianization is exactly the right size. Dropping to the full group
carries redundant information (`gamma` is never needed); dropping to either
single bit loses the claim, with explicit witnesses. This kills the "activity
parity flux" idea — the proposal that a 1-bit activity coordinate suffices —
by counterexample: at `W=21212122`, tail 2, row 2, the activity bit is constant
across the entire scenario chain while the pair is not.

## 4b. The Mersenne-tightness hypothesis is refuted

Rule 90's C3 failures sit exactly at `n = 2^r - 1`, and the two tight Rule 30
rows sit at `n = 3 = 2^2 - 1`. That invites the reading that C3ab is tight
precisely where Rule 90's linear cancellation bites, and that Rule 30 barely
escapes there. Tested by taking the minimum C3ab slack `max S_j^ab - j` per
source length:

```text
 n   Mersenne   legal rows   min slack (ab)   rows at min   min slack (full)
 1     YES              0         -                  0          -
 2                      1         1                  1          1
 3     YES              7         0                  2          0
 4                     11         1                  2          1
 5                      4         4                  4          4
 6                     13         4                  6          4
 7     YES             55         3                 11          3
 8                     53         5                 51          5
 9                     84         2                  5          2
10                    126         5                 15          5
11                    247         7                 17          7
12                    363         7                 30          7
13                    476         8                  2          8
14                    946         5                  3          7
15     YES           1425         8                  2          8
```

There is no Mersenne dip. `n = 7` has minimum slack 3 while `n = 9` has 2;
`n = 15` has 8 while `n = 14` has 5. `n = 1` carries no legal rows at all. The
only tight length is `n = 3`, and it is tight because it is small, not because
it is `2^2 - 1`.

The table also says something more useful than the refutation: **the minimum
slack grows with `n`**, from 0-1 at `n <= 4` to 7-8 by `n = 13..15`. C3ab is not
on a knife edge that a longer word might tip over; it gets safer as `n` grows.
That is weak evidence the strengthening is not a trap, and it is the opposite of
what a "Rule 30 barely escapes at Mersenne lengths" picture predicts.

## 4c. Stratify by `L = n - j`, not by `n`: the tight set is explained

Grouping every legal row by the remaining suffix length `L = n - j` rather than
by source length, over all hard-core words to `n = 16`, both tails:

```text
 L   legal rows   min slack   tight rows   first tight
 1            2           0            2   W=121, tail 3, row 2
 2            3           1            0
 3           13           1            0
 4           14           1            0
 5           21           3            0
 6           45           4            0
 7           63           5            0
 8           75           5            0
 9          116           7            0
10          217           7            0
11          337           9            0
12          520           6            0
13          785          11            0
14         1117           9            0
15         1489          12            0
16         1382          12            0
```

Two things fall out.

**The tight set is forced, not mysterious.** At `L = 1` the only token with
`k >= j` is `k = j` itself, so the slack is either 0 or the row is a failure.
Slack 0 is the *only* non-failing outcome at `L = 1`. The two tight rows are
tight because they are the only `L = 1` legal rows in the corpus, not because
`n = 3`. This supersedes the Mersenne reading of section 4b: `n = 3 = 2^2 - 1`
is incidental, and `L` is the variable that governs.

**`L = 1` legal rows exist exactly when `(1)` is tight.** A legal row with
`L = 1` means `j = n - 1`, which for tail 2 needs `s_2 >= n` and for tail 3
needs `s_3 >= n + 1`. Measured, `max(s_2 - n) = -1`, so tail 2 can never reach
it; and `s_3 = n + 1` holds only at `W = 121` and `W = 221`. So the tight rows
of C3ab are precisely the words attaining the bound they are used to prove.

**Consequence for the proof.** The induction should run on `L`, not on `n`: the
minimum slack tracks `L` (roughly `3L/4` over this range) and not the source
length. The base case is `L = 1`, which is two explicit rows. A violation of
`(1)` is exactly a legal row with `L <= 0` — an empty remaining suffix, for
which `f` has a single scenario and is constant for free. That is the same
two-line implication as section 3, seen concretely: `C3ab` fails at `L = 0` by
definition, so proving `L >= 1` on legal rows *is* proving `(1)`.

## 4d. `n = 21` clears the derivative death length

Scored with a fast path that reads `(alpha, beta)` straight off the frozen
`bitsliced_trace_states` affine and drops only `gamma` — validated by assertion
against the slow path on every hard-core word to length 12, per-length minima
identical:

```text
through length 21:  72,351 legal rows,  C3ab failures 0
n = 21 alone:       28,146 rows,  min slack 9 (attained on 104 rows)
tight rows (slack 0), whole corpus:  exactly W = 121 and W = 221, tail 3, row 2
```

The pointwise-derivative certificate passed to 16 and broke at 21. C3ab does
not break at 21, and the tight set is unchanged from `n = 3`.

## 4e. The kernel is NOT empty, and that is the real structure

`f` depends on `(V, j, c)` and on nothing else: every scenario in the chain has
`k >= j`, so `W[:j]` is zeroed in all of them and cannot matter. It does **not**
depend on `V` alone — `j` matters. Dumping the constant-`f` triples for
hard-core `V` of length `<= 5`, `j <= 14`, both tails, legality ignored:

```text
V=1     c=2 j=6,10        V=2      c=2 j=7,8,10      V=12    c=2 j=5
V=1     c=3 j=5,9,11      V=2      c=3 j=3,6,9,10    V=21    c=2 j=0,11
V=22    c=2 j=3           V=122    c=3 j=4           V=21    c=3 j=0
V=2122  c=2 j=12          V=21221  c=3 j=7
```

So there are nonempty hard-core suffixes whose abelian pair is frozen along the
entire nested chain. `K = {V : f constant}` is not `{empty word}`, and no proof
of the form "f can never be constant on a nonempty hard-core V" exists.

**But not one of them is reachable on a legal row.** For each triple with
`n = j + |V| <= 18`, enumerating every hard-core `W` of length `n` with
`W[j:] = V`:

```text
20 triples, 1,465 realizing words in total, 0 of them legal at row j.
```

This is an independent confirmation of C3ab computed the other way round — from
the suffix side with the slow path, checked against the fast census — and it
finds no contradiction.

**Consequence, and it corrects the natural proof plan.** C3ab is not a statement
that `f` is never constant. It is:

> No hard-core `W` has a legal row `j` whose remaining suffix triple
> `(W[j:], j, c)` lies in `K`.

The obstruction is **reachability**, not the algebra of `f`. The dangerous
configurations exist; survival always runs out before they can be reached. A
proof has to show that the forced continuation dies before any `K` triple
becomes legal, which is a statement about survival and legality, not about
whether two GF(2) bits can freeze.

### 4e.1 Where in the illegal region: `s - j` measured

For every realizing word of every `K` triple with `n <= 18`, the histogram of
`s - j` (survival minus the freeze row):

```text
s-j:   -12  -11  -10   -9   -8   -7   -6   -5   -4   -3   -2   -1    0    1
words  198  431  278  195  140   99   51   22   18   18   10    3    1    1
```

1,463 of 1,465 realizing words have `s - j <= -1`.

**This pooled table does not identify a mechanism, and an earlier draft of this
section wrongly read one off it.** "Dead for 6 to 12 rows before the freeze"
does not follow: if `s = 0` then `s - j = -j`, which reproduces the histogram
exactly, and the visible mass sits at the `j` values of the 20 triples. A pooled
statistic over triples with different `j` cannot separate a chasing gap from
immediate death. See 4e.1a for the unpooled table, which refutes both readings.

The two boundary words are both `W = 21`, `n = 2`, `V = 21`, `j = 0`:

```text
tail 2:  s = 0,  s-j = 0   the first forced symbol is 3, so the row never exists
tail 3:  s = 1,  s-j = 1   j = s-1, the exempt tail-3 final row
```

So the tail-3 exemption **is** occupied by a `K` triple, but by exactly one, at
`n = 2`. The exemption is not the general mechanism; it is one degenerate cell.

### 4e.1a Unpooled: survival per triple, and both clean readings die

For each `K` triple, over its realizing words: the range of `s`, how many
distinct values it takes, and the distribution of the **first** forced symbol.

```text
  V        c   j  words  min_s max_s #s   first forced symbol
  1        2   6    13      0     4   3   1:1,2:5,3:7
  1        2  10    89      0     3   4   0:12,1:25,2:28,3:24
  1        3   5     8      0     2   3   0:2,2:4,3:2
  1        3   9    55      0     2   3   0:19,1:14,2:14,3:8
  1        3  11   144      0     5   6   0:73,1:27,2:30,3:14
  2        2   7    34      0     3   4   0:11,1:8,2:8,3:7
  2        2   8    55      0     2   3   0:29,1:15,2:2,3:9
  2        2  10   144      0     4   5   0:41,1:28,2:42,3:33
  2        3   3     5      0     0   1   0:3,3:2
  2        3   6    21      0     4   4   0:4,1:7,2:5,3:5
  2        3   9    89      0     6   6   0:15,1:19,2:31,3:24
  2        3  10   144      0     4   5   0:28,1:41,2:33,3:42
  12       2   5     8      0     1   2   0:2,1:2,2:3,3:1
  21       2   0     1      0     0   1   3:1
  21       2  11   233      0     3   4   0:49,1:83,2:33,3:68
  21       3   0     1      1     1   1   2:1
  22       2   3     5      0     1   2   0:3,1:2
  122      3   4     5      0     3   2   2:3,3:2
  2122     2  12   377      0    10   6   0:116,1:88,2:91,3:82
  21221    3   7    34      0     2   3   0:16,1:6,2:9,3:3
```

**Immediate fatality is false.** `min s = 0` everywhere (except the `j = 0`
tail-3 cell), but `max s` reaches 10, and `s` takes up to 6 distinct values over
the prefixes `P`. Survival genuinely spreads with `P`; it is not a function of
`V` and `c` alone.

**The first-symbol identity is false.** In 16 of 20 triples the first forced
symbol takes all four values across the realizing prefixes. Death is not at step
0 for all `P`, so "Freeze(V,j,c) implies the first forced symbol of every `P.V`
is 0 or 3" is refuted directly.

**What is true, and it is the hard branch.** `max s` stays strictly below the
legality threshold in every triple, but with a varying and sometimes small
margin. The tightest is `V = 2122`, `c = 2`, `j = 12`, `n = 16`: `s` reaches 10
against a threshold of 12. So the surviving statement is a genuine bound on
survival over the whole prefix class, not a local identity and not a constant.

### 4e.2 This refutes the local-identity plan and flags a stronger-than-target step

Two candidate mechanisms were on the table. The data picks against the clean one.

- **"Freeze implies death within a window", by a local identity on the 4x4
  table** — refuted. The gap is not a window. Freeze rows sit up to 12 rows past
  death, so no statement of the form "a frozen `(alpha,beta)` pair can emit at
  most one more hard-core symbol" can be what is going on.
- **"Death implies freeze is unreachable", by bounding `s` for these `V`** — this
  is what the shape of the data suggests, and it carries a specific hazard worth
  stating before anyone writes it.

The hazard, precisely. C3ab needs, for a `K` triple, that row `j` is illegal,
i.e. roughly `s < j = n - L`. The conjecture `(1)` only gives `s <= n`. So the
reachability route requires a bound **strictly stronger than the target**, on a
restricted class of words. That is not automatically circular — the class is
restricted and the charge could differ — but any argument that reaches it by way
of `s <= n` is circular and must be discarded. The circularity test stands: if a
proof says "`s <= n`, therefore the freeze row is illegal", it is assuming `(1)`.

Neither branch is closed. What is closed is the reading that a short local
identity on the action table will do it.

## 4f. Is `K` finite? Inconclusive, and the strategy dies anyway

Maximum freeze-suffix length over hard-core `V` with `|V| <= 8`, by row depth:

```text
 j    maxL(c=2)  maxL(c=3)   #K triples   longest V
 0        2          2            2       21   c=2
 1        0          0            0
 2        0          0            0
 3        2          1            2       22   c=2
 4        0          3            1       122  c=3
 5        2          1            2       12   c=2
 6        1          1            2       1    c=2
 7        1          5            2       21221 c=3
 8        1          0            1       2    c=2
 9        0          1            2       1    c=3
10        1          1            3       1    c=2
11        2          1            2       21   c=2
12        4          0            1       2122 c=2
13        0          0            0
14        0          0            0
```

`max L` does not grow with `j`: it wanders between 0 and 5 with no trend, and
four values of `j` carry no freeze triple at all. `K` is very sparse, at most 3
triples per row depth.

This is **not** a finiteness result. Fifteen row depths with a wandering maximum
of 2 to 5, searched only to `|V| <= 8`, cannot distinguish a finite poison list
from a slowly growing one. The check was run to decide whether a table-shaped
argument is possible, and it returns "not excluded", which is the weakest useful
answer.

## 4g. Route disposition: the reachability restatement does not localize

Stated plainly, because the measurements above are facts and the strategy built
on them is not.

C3ab is true as far as measured and remains a valid reduction: `C3ab ==> C3 ==>
(1)` is two lines plus a homomorphism, and it holds on 72,351 legal rows through
`n = 21`. None of that is retracted.

What is dead is the hope that the reachability form localizes. After the
relocations of this file, C3ab says: for every freeze triple `(V, j, c)` and
every hard-core prefix `P` of length `j`, `s_c(P.V)` is below the legality
threshold at `j`. Every candidate local mechanism for that has now been refuted
by measurement:

- immediate fatality `s = 0` (4e.1a: `max s` reaches 10);
- a first-symbol identity (4e.1a: 16 of 20 triples take all four first symbols);
- a chasing gap tracking `j` (4e.1a: `max s` is 3 and 5 at `j = 11`, 6 at `j = 9`);
- "frozen pair emits at most one more hard-core symbol" (4e.2);
- any bound routed through `s <= n`, which is `(1)` assuming itself.

The structural reason they all fail is worth recording. The freeze is
**`P`-independent**: every scenario in the chain has `k >= j` and therefore
zeroes all of `P`. The survival `s_c(P.V)` is **`P`-dependent**, and its first
forced symbol is almost entirely a function of `P`. So the statement asks a
`P`-independent abelian fact to bound a `P`-dependent lifetime, and no quantity
shared by the two processes has been found. On the restricted class the required
bound (`s < j = n - L`) is also *stricter* than `(1)` itself, so this is not a
reduction in difficulty, only in vocabulary.

The honest disposition: **this is a `K`** — the mechanism class "prove `(1)` by
localizing C3ab's reachability form" is closed, while C3ab itself stays open and
true-so-far. Anyone resuming should either name a quantity shared between the
nested zero-prefix chain of `V` and the lifetime of `P.V` before writing code,
or treat the abelianization as a structural finding about the coordinates rather
than as a proof route.

## 5. What this says about the Rule 90 dependency

It runs against the natural reading, and against the outside proposal that
prompted it.

Rule 90's newest-cut group **is** `Z2 x Z2`, abelian of order 4. Rule 30's
abelianization is also `Z2 x Z2`. If C3 for Rule 30 already holds in that
quotient, then the statement being proved has the same target group as the Rule
90 case — and Rule 90's version of C3 fails, at exactly the lengths `2^r - 1`
(`RESULTS-C14-KILL-AND-RULE90-CONTROL.md` sec. 2.2a).

So non-commutativity of the codomain cannot be where the Rule 30 dependency
lives. C3's truth does not need `gamma`, and `gamma` is the only non-abelian
part. The dependency must instead sit in **how the source determines the
phi-image** — that is, in the nonlinear map from source word to edge states,
whose generator is `activity = hi OR lo`. That OR is the same one that produces
`Phi(2,.) = Phi(3,.)`.

This is a narrowing, not a proof: it says a correct argument must use the OR in
the *state recursion*, and may not appeal to non-commutativity of the group.

## 6. Horizon and honest limits

- The horizon is length 21, per sections 4 and 4d. C3ab could fail at a larger length
  exactly as the pointwise-derivative certificate passed to 16 and broke at 21 —
  and being the *stronger* claim, it is the more likely of the two to break.
- C3ab being true does **not** make the problem linear. Only the final
  composition is abelianized; the edge states are still a nonlinear function of
  the source.
- This does not prove C3, C3ab, or `(1)`. It replaces one unproved statement
  with a stronger unproved statement over a smaller object, and rules out one
  class of intended mechanism.

## 7. Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 uv run python \
  experiments/rule30/p1-period2-invariant/c3_abelianization_probe.py \
  --max-length 18
```
