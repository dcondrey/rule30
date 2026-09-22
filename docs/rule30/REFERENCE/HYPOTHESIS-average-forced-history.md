# A new target: average forced bits in a chronological ancestor class

Date: 2026-09-12. **Proposed hypothesis, not a uniform theorem.**

The proposed estimate is

\[
\boxed{2\sum_{w\in C_r(\alpha)} f_{r,\alpha}(w)
       \ \ge\ D(\alpha)\,|C_r(\alpha)|.}                 \tag{H}
\]

Here f is a precise decoding statistic defined below. The conjecture says
that the **average** ancestor permits at least one forced-bit omission per
two cumulative repeats. It imposes no requirement of new omissions at the
moment a repeat occurs.

If proved uniformly, (H) gives the sufficient counting estimate with c=1 and
epsilon=1/2, and therefore finite-frontier mortality and period-two exclusion.
The hypothesis remains unproved beyond the certified ranges below. No
singleton-seed reachability, arbitrary-period exclusion, or P2 conclusion is
claimed.

## 1. Exact definition of the new statistic

Fix the original length r, the complete chronological tape alpha, and its
exact class C=C_r(alpha), including **every** intermediate guard. Write the
m=2r-1 free original bits in this fixed reading order:

```
b_(r-1), a_(r-1), b_(r-2), a_(r-2), ..., b_1, a_1, b_0.
```

The legal a_0=1 is not a free bit and receives no credit. For each w in C,
read these bits in order. At a position, retain all members of C agreeing
with the values of w already read.

* If both values of the next bit occur in this remaining set, write the
  actual bit of w into the code.
* If only one value occurs, infer that value and omit it from the code.

Let f_(r,alpha)(w) be the total number of omitted, forced bits. This is a
property of the **full original history class**, not a test on arbitrary
current predecessors. The set of omitted coordinates can differ between
ancestors. Determining a bit can depend on an arbitrarily long already-read
suffix and on all the chronological guards.

For C empty, both sides of (H) are zero. The empty tape also satisfies (H):
the class is the full legal cube and f=0.

No average monotonicity is assumed when C is narrowed. For a retained w its
forced-bit count cannot decrease, but changing the population can change its
average in either direction. When the entire original class stays fixed on
a plateau, every f and its average stay fixed too. Previously acquired
omissions must then pay for subsequent repeats.

## 2. Why the average is enough: a proved coding lemma

The decoder knows r and alpha and follows the same rule, requesting a code
bit exactly when both continuations are possible. This recovers the unique
original. Contracting the forced edges of the binary prefix tree gives a
full binary tree whose leaves are the members of C. The codeword for w has
length m-f(w), and the code is prefix free. Consequently

\[
\sum_{w\in C}2^{-(m-f(w))}=1,
\qquad \sum_{w\in C}2^{f(w)}=2^m.                       \tag{1}
\]

The arithmetic-geometric mean inequality gives, with
`f_bar=(sum_C f)/|C|`,

\[
|C|2^{\bar f}\le\sum_{w\in C}2^{f(w)}=2^m.
\]

Thus **(H) would imply**

\[
|C_r(\alpha)|\le2^{2r-1-D(\alpha)/2}.                  \tag{2}
\]

This is a proved implication, not a proof of (H). A nonempty class would
then have D<=4r-2. The established repeat lower bound would give

```
N <= 2^(4r-1)(r+2)-r-1,
```

which is finite for each original length. Sharp constants are unnecessary.

The hypothesis is not a general coding fact disguised as a Rule 30 claim.
For the set of all 2k-bit words with exactly k ones, the same decoding rule
forces precisely the final monochromatic run. Its mean is

```
2 * SUM_(j=1..k) binomial(2k-j,k) / binomial(2k,k)
    = 2k/(k+1) < 2,
```

although its counting information `2k-log_2 binomial(2k,k)` is unbounded.
Thus there is no general positive fraction of counting information supplied
by mean forced bits. Establishing (H) requires a property of the actual
guarded Rule 30 reconstruction languages.

## 3. Why this survives the known objections

This target uses a global, ancestor-dependent decoder. It is not fixed
coordinate deletion, a collection of globally valid affine equations, or a
bounded-arity support envelope. The earlier obstructions to those methods
therefore do not apply. In particular, full low-order projections do not
prevent a bit from becoming forced after many other original bits have
already been read.

For the full 36-member plateau at length six, the sum of forced bits is 204,
so the mean is 17/3 throughout tapes `101` through `1011100`. The three later
repeats consume some of this earlier information without changing the class.

For the established length-24 tape `00011100001111111100`, D=15 and

```
|C| = 55,885,140,
SUM_C f = 1,102,039,992,
f_bar = 1,133,786 / 57,495 = 19.719732... .
```

The proposed threshold is only 7.5. All eight plateau repeats are included.
This is a preflight check of a known difficult class, not evidence of a
uniform theorem by itself.

## 4. A stronger first version was tested and rejected

Requiring `min_(w in C) f(w) >= D/2` would also imply (2), but is false.
The new targeted test finds

```
r=31, alpha=00000000, D=7,
w=2030120000000201112030300010020,
f(w)=3.
```

The certificate supplies 58 alternative originals. At each of 58 reading
positions, its alternative agrees with w at every earlier-read position
and flips that position, while still emitting all eight zeros successfully.
Therefore at most three of the 61 original free bits can be forced along
this decoding path. All 59 originals are independently replayed through
every guard with the frozen oracle. This refutes the minimum-path version
without relying on a computed absence of other ancestors.

The average on this class is

```
31,802,668,016,107 / 2,486,247,551,586 > 12,
```

so it does not refute (H). Passing to an average uses exactly what the
coding lemma permits; the constant 1/2 has not been adjusted to evade this
witness. The minimum version must not be reused as a proposed theorem.

## 5. An exact reverse automaton makes the hypothesis testable

The following closure is an all-depth algebraic result. It provides a
different calculation of the new statistic from the original-variable BDD.

Use the [common temporal column](RESULTS-cumulative-history-transfer.md)
encoded with A_0 at bit zero, B_1 at bit one, A_1 at bit two, and so on.
Represent a pair of possible incoming columns as

```
P(q,tau) = {q, q XOR 1 XOR (2*tau)},    q even, tau in {0,1}.
```

There are 2*4^n such pair states at temporal depth n. The accepting pair for
the complete guarded tape alpha is initially P(sigma(alpha),0).

When an original suffix symbol `x=2a+b` is read from right to left, its high
bit selects the target column

```
y = q XOR (a*(1+2*tau)).
```

Invert the exact column recurrence with old A_0=0 and input x:

```
A_j = A'_j XOR (B'_j OR A'_(j-1)),
B_j = B'_j XOR (A_(j-1) OR B'_(j-1)).
```

Call the resulting even column q'. If old A_0 is changed to one, only old
B_1 can also change, and its change is 1-b. All higher old high coordinates
are independent of old A_0, so all higher old low coordinates are too.
The exact next pair is therefore

```
R_x(q,tau) = (q', 1-b).                                  (3)
```

This proves closure of the pair representation under every fixed suffix
symbol, with no powerset relaxation or fresh completion of a current orbit.
After reading the r-1 non-origin symbols, the incoming-high-one column must
equal one of the two true origin columns o_0,o_1. At most one fits, and it
determines b_0. The starting signature retained every chronological guard,
so this is exactly an automaton for the original class C_r(alpha).

Let G_k(s) count accepted remaining original prefixes consisting of k
non-origin sites plus the origin. Let Q_k(s) sum their remaining forced-bit
counts. Initially G_0 is one at each of the four origin-compatible pair
states and zero elsewhere; Q_0=G_0, because b_0 is forced there.

At a pair state s put `g_ab=G_k(R_(2a+b)(s))`. A low-bit value b is possible
if some g_ab is positive. Let ell=1 if only one b is possible, and h_b=1 if
only one a is possible for that b. Impossible branches contribute zero.
Then the exact integer recurrences are

```
G_(k+1)(s) = SUM_(a,b) g_ab,
Q_(k+1)(s) = SUM_(a,b) [Q_k(R_(2a+b)(s)) + g_ab*(ell+h_b)]. (4)
```

For the original problem,

```
G_(r-1)(sigma(alpha),0) = |C_r(alpha)|,
Q_(r-1)(sigma(alpha),0) = SUM_(w in C_r(alpha)) f(w).
```

Thus (H) is a precise inequality between two explicitly generated integer
arrays. It assumes neither independent guards nor balanced branch counts.

There is also an exact stopping certificate at each fixed tape depth. Once
every G_k(s)>0, both bit values are available at both positions of each
symbol, so all new ell and h_b vanish. Thereafter G and Q obey the same
positive linear transfer. If at that stage

```
2 Q_k(s) >= (n-1) G_k(s) for every pair state s,           (5)
```

the inequality persists for every larger original length. Since D<=n-1,
checking the finitely many earlier lengths plus (5) certifies (H) for all
original lengths at that temporal depth.

## 6. Completed preflight and depth-ten test

The [probe](../../experiments/rule30/average_forced_history_probe.py),
[BDD statistic](../../experiments/rule30/average_forced_history_probe.cpp)
and [saved artifact](../../experiments/rule30/average-forced-history-probe.json)
provide exact checks:

* The reverse recurrence certifies (H) for **every original length and every
  tape of length at most nine**. Its tail cutoffs at depths 1 through 9 are
  `3,6,8,11,13,16,19,22,25`. The finite prefix contains 22,574 tape/length
  comparisons; these are transfer coefficients, not original-frontier scans.
* The new statistic passes on 477 records from the seven already counted
  continuation trees. Every original ancestor count matches the saved prior
  artifact. This does not add new starting-length census coverage.
* Separate reverse-automaton calculations match both G and Q at all seven
  nine-symbol roots, including original length 35. Explicit tries of the
  saved 36 original words independently check the BDD forcing recurrence.
* The minimum-path counterexample has an independent 59-original, 472-guard
  replay and an independent forward-transfer count.

Run with

```sh
uv run --no-project python experiments/rule30/average_forced_history_probe.py
```

The completed local run took about 12 seconds. Integer overflow is checked
before array arithmetic, native subprocesses have external wall timeouts,
and incomplete outputs are not accepted. No paid computation, seed
regeneration, or large original-frontier enumeration is involved.

**Completed, 2026-09-12:** the preregistered depth-ten falsification test
passed within its original 64-transfer, 60-second, 1-GiB limits. It checks
28,672 tape/length pairs through original length 28. At that length all
2,097,152 reverse states have positive counts and the minimum surplus
`2Q-9G` is 14,234,187,024. The positive-cone argument therefore proves (H)
at depth ten for every larger original length too. Selected G and Q values
have independent BDD checks. The
[contract and result report](RESULTS-average-forcing-lift.md) gives the
exact values and links to the saved artifacts.

The stopping rule was followed: no depth eleven test was started. The uniform
proof attempt instead proves an all-depth factorization of the reverse graph
through the existing forward graph, a tape-independent spatial limit mu_n
for the mean forced count, and an exact four-way temporal partition law.
It proves mu_n is nondecreasing, but not the needed linear lower rate.
An actual length-29 class also shows that the conditional mean can decrease
at a repeat. See the same report for the proofs and exact verifier.

The positive-cone route would still need (5) at a suitable cutoff at every
temporal depth, plus the valid-signature inequalities before that cutoff.
Neither uniform assertion is currently proved. The hypothesis's coding
implication has exponent 1/2. A separate deduction from the stronger saved
finite-range means and the earlier six-symbol spatial tail certificate also
proves the **original exponent-one inequality for all original lengths at
tape lengths at most ten**. That deduction uses only saved certificates;
it does not extend the result to unbounded tape length.

The purpose of this proposal is to give the missing cumulative-information
question a concrete global coding statistic and an exact reverse recurrence.
It is not a claim that the remaining induction is known or nearly proved.
