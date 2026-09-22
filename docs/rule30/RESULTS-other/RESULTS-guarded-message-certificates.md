# Exact upper messages that retain coupled chronological guards

Date: 2026-09-13. **A certificate construction and bounded comparisons, not
an unrestricted counting proof.** The proposed cumulative inequality,
finite-frontier mortality, and period-two center exclusion remain open.

This implements the graphical-model route in the
[method assessment](NOTE-ml-method-selection.md). The substantive results are:

- a least-upper-envelope theorem for messages expressed as a minimum of
  overlapping coordinate tables;
- exact upper certificates on three saved history examples, including a
  20-scalar plateau with 15 repeats;
- a verified benefit from retaining separated temporal layers and contracting
  the fixed original boundary exactly;
- proofs excluding specified simpler message families, with their limitations
  stated separately below.

The example inequalities were already known by other methods. The new result
is that the specified compressed messages certify them, and that competing
message choices provably lose necessary precision. This does not extend the
known general range of the counting conjecture.

All counts concern legal **original** auxiliary frontiers at a fixed length r.
No singleton-seed reachability is assumed. No frontier census was extended.

## 1. Exact factor elimination and the certificate obligation

The hard-constraint factorization in the method assessment has one complete
assignment for each original frontier emitting the prescribed tape, and none
for any other original. Eliminating its spatial columns gives the existing
[exact transfer](RESULTS-cumulative-history-transfer.md), which we reuse.

At temporal depth n a separator is

```
q = (A_0,A_1,B_1,...,A_n,B_n) in {0,1}^{2n+1}.
(T f)(q) = SUM_(x=0..3) f(delta(q,x)).
```

The local cascade defining delta is exactly the supplied bulk rule. The
terminal indicator g_alpha is supported on the two signatures returned by
`signature(alpha)`, differing only in A_0. It retains **every** chronological
guard and transported birth suffix. If o_beta is the column after the first
legal original symbol 2+beta, then

```
G_r(alpha) = SUM_(beta=0,1) (T^(r-1) g_alpha)(o_beta).
```

There are two choices at the first original symbol and four at each later
one. Intermediate rows, born symbols, and repeats introduce no new counting
weight or prior. Thus the denominator is exactly 2*4^(r-1).

Choose bags S_j of temporal pairs, each also retaining A_0. For its projection
pi_j, define

```
(L_j u)(q) = u(pi_j(q)),
(M_j F)(z) = MAX_(q: pi_j(q)=z) F(q),
(C F)(q) = MIN_j (L_j M_j F)(q).
```

The message class consists of functions H=MIN_j L_j u_j. Different bags may
overlap. This is a pointwise envelope, not an assertion of independence.

**Least-majorant theorem.** C F is the pointwise least function in this class
that majorizes F. Indeed

```
MIN_j L_j u_j >= F
iff EVERY L_j u_j >= F
iff EVERY u_j >= M_j F.
```

Choosing equality in all the last inequalities proves the claim. C is
monotone and idempotent. Consequently

```
H_0 = C g_alpha,       H_(ell+1) = C T H_ell
```

is a valid upper sequence and the pointwise smallest sequence in this class
obeying these **stepwise local** inequalities. If the bags collectively cover
all temporal pairs, H_0=g_alpha exactly: no guard has been removed at the
terminal factor.

This optimality has a precise scope. It does not say that H_ell is the least
representable majorant of the exact T^ell g_alpha. Earlier projections can
lose information. Delaying a projection, changing the bags, or grouping
transfers can improve the bound. Merely optimizing table values within the
same stepwise certificate class cannot improve its canonical envelope.

The checker tests proposed tables against the complete separator, requiring

```
MIN_j u_(ell+1,j)(pi_j(q)) >= SUM_x H_ell(delta(q,x))
```

at every q. The sum uses one common full state q for all four inputs. Taking
a separate hidden-state maximizer for each input would give a different,
looser relaxation. All arithmetic here is integer and range-checked.

## 2. Use the actual original boundary before projecting again

For any b between zero and r-1, a valid bound is

```
G_r(alpha) <= SUM_beta (T^b H_(r-1-b))(o_beta).
```

The last b transfers can be contracted exactly at the two actual origins;
they need not be projected onto bags first. Since C F>=F, increasing this
exact boundary block cannot increase the resulting bound, when the earlier
canonical messages and bags are otherwise unchanged.

The verifier evaluates b=0,1,2,3 using exact integer multiplicities on the
reachable separator states. Total boundary weight is 2*4^b. These are the
first original symbols in the same count, not fresh current predecessors.

A small discriminator proves that grouping can matter. For n=3, alpha=`000`,
r=4, and singleton-pair bags, the stepwise upper count is 30. Computing three
exact transfers before one projection gives upper count zero, equal to the
actual count. Thus a failed stepwise certificate must not be reported as a
failure of all messages with those bags.

## 3. Bounded certificate comparisons

All layer indices below are one-based temporal pair indices. Every bag also
retains A_0. A width-k window contains k consecutive temporal pairs, and the
window family contains all such windows.

For original length 14 and alpha=`00001111`, D=6 and the required one-bit
threshold is 2^21=2,097,152. The previously verified exact count is 196,488.

| Window width | Entries per message level | Upper count, projecting every step | Upper count, three exact origin steps |
|---:|---:|---:|---:|
| 1 | 64 | 32,839,186 | 32,696,448 |
| 2 | 224 | 6,219,076 | 2,317,242 |
| 3 | 768 | 1,249,176 | 394,128 |
| 4 | 2,560 | 216,684 | 216,684 |
| 5 | 8,192 | 196,488 | 196,488 |

The full separator has 131,072 states. Width three suffices for this
inequality; width five recovers the exact root count. This does not imply
that every intermediate width-five message is exact. The checker still
visits the full separator, so table compression alone has not supplied a
uniformly efficient checking algorithm.

For the plateau example, let

```
r = 24,
alpha = 00011100001111111100 = 0^3 1^3 0^4 1^8 0^2,
D(alpha) = 15,
beta = alpha[:9] = 000111000.
```

The [saved exact counts](RESULTS-weighted-history-endpoints.md) are
G_24(alpha)=55,885,140 and G_24(beta)=380,628,720. They are different classes.
We certify an upper bound for beta and use the exact inclusion
C_24(alpha) subset C_24(beta). This deliberately relaxes later guards for an
**upper** bound; it does not assert that beta alone proves later ancestry.
The full tape's one-bit threshold is 2^47/2^15=2^32=4,294,967,296.

| Bag choice on the nine-layer prefix | Entries per level | All steps projected | Three exact origin steps |
|---|---:|---:|---:|
| All width-seven windows | 98,304 | 5,094,846,684 | 3,741,235,704 |
| Those windows plus (1,2,3,4,7,8,9) | 131,072 | 4,051,343,556 | **2,705,778,216** |
| All width-eight windows | 262,144 | 951,964,326 | 895,675,266 |

The full nine-layer separator has 524,288 states. Contiguous width-seven
messages alone miss the threshold if projected at every step. Either the
separated-layer bag or three exact origin transfers repairs that failure;
using both improves the upper bound further. The narrower messages still
greatly overcount the actual class, but now in a rigorously useful direction.

The length-six plateau `1011100` is another control: singleton, width-two,
and width-three windows give 168, 52, and 36 before exact boundary grouping.
Width two plus two exact origin steps already gives its known exact count 36.
No per-repeat loss of ancestors is presumed.

## 4. An all-original-length tail certificate for the r=87 example

For alpha=`001001111`, use all width-three windows. At 17 spatial transfers
the certified message's global normalized maximum is

```
MAX_q H_17(q) / 4^17 = 109826419 / 8589934592 < 1/32.
```

Normalized transfer P=T/4 preserves constants. Therefore the same upper
probability holds for every original r>=18, by propagating that constant
majorant through all remaining original symbols. This includes r=87 and
certifies its D=5 upper-count inequality without constructing a depth-87
object or enumerating its ancestors.

This example was already covered by the bounded-tape theorem; the new
certificate uses 896 message entries per level. It proves neither the
split-value ambiguity lower bound nor a uniform repeat bound on continuations.

## 5. Exact obstructions that narrow the message search

**Prefix-only projection.** If a single bag retains A_0 and precisely the
first k temporal pairs, the triangular cascade commutes with that projection.
Maximizing the terminal indicator over all other pairs gives exactly the
indicator for alpha[:k]. All subsequent messages are the depth-k exact
transfer. Its root bound is therefore exactly G_r(alpha[:k]), regardless
of later guards or repeats. This family cannot produce a uniform positive
repeat rate with fixed k: for arbitrarily long constant tapes, take original
r large enough that the prefix probability is close to its positive
spatial limit 4^(-k).

**Single terminal window.** The separate
[terminal-window theorem](RESULTS-terminal-window-message-obstruction.md)
proves that retaining A_0 and the last k pairs, and maximizing over at least
three earlier pairs after every transfer, gives upper probability exactly
one once r-1>=2*(4^k-1). Its local channel proof and exact verifier cover
arbitrary k. This does not exclude the coupled minimum used above.

**Nonnegative additive bags.** The
[additive-message theorem](RESULTS-additive-message-obstruction.md) proves a
stationary mean floor 2^(-k-2b) for any nonnegative sum of functions of at
most k bits majorizing the message after b exact transfers. Arbitrarily many
such bags, even chosen according to the spatial horizon, do not remove the
floor when k,b stay bounded. Minima, products, and signed decompositions are
outside that theorem's hypotheses.

**Precision floors inside the tested minimum class.** If a canonical message
has minimum m>0 after ell transfers, then every later message is at least
4^s*m after s further transfers. Its normalized origin bound has permanent
floor m/4^ell. For the eight-layer `00001111` example, singleton windows
reach floor 239/1024 at ell=8, and width-two windows reach 5895/131072 at
ell=12. Both exceed 1/64. Consequently further stepwise propagation cannot
make those respective families certify this tape's one-bit bound. With an
exact boundary block of fixed length b, the same argument applies once
the remaining compressed horizon exceeds the stated ell. These are
fixed-depth obstructions, not an all-depth impossibility for minimum messages.

## 6. Verification, limits, and next mathematical obligation

Files:

- [Primary exact checker](../../experiments/rule30/guarded_message_certificate.py)
  and [artifact](../../experiments/rule30/guarded-message-certificate.json).
- [Independent message implementation](../../experiments/rule30/guarded_message_independent_audit.py)
  and [artifact](../../experiments/rule30/guarded-message-independent-audit.json).

Run either verifier with `uv run --no-project python PATH`. The primary
completed twelve bounded configurations in about two seconds, checking
56,950,784 pointwise upper inequalities. It checked 512 small-depth column
edges against a separate scalar-loop implementation, rejected an invalid
message, and used 37 frozen-oracle update attempts on ten targeted original
words to check the guarded-signature representation. The independent
implementation reproduces the main numerical comparisons and grouping
control. Both use integer comparisons; no floating-point fit supports a claim.

The code bounds temporal depth, original length, arithmetic range, and wall
time. Its output is written only after all checks pass. Message hashes make
the generated tables reproducible; they are not substitutes for checking the
inequalities. The independent message implementation reuses the established
column graph, so it is an independent audit of the message computation, not
a second all-depth derivation of that graph. The frozen trajectory controls
serve the separate membership check.

These tests make one design decision concrete: retain coupled constraints
and use the actual original boundary before discarding information. They
also show that table-value learning alone cannot improve the optimal
stepwise envelope; it would have to propose different bags, grouped
contractions, or a richer representation.

What remains is an inequality uniform in temporal depth and original length
for such certificates, with root probability at most c*2^(-epsilon*D) for
fixed c,epsilon>0, or an exact counterexample to the original conjecture.
No such uniform certificate is constructed here. The present family has
not been proved sufficient or impossible at all depths. Period two remains
unexcluded by this investigation.

**All-length follow-up, 2026-09-13.** The
[coupled-message depth audit](RESULTS-coupled-message-depth-audit.md) now
proves that all contiguous-window families of widths one, two, and three,
with projection after every spatial transfer, fail every uniform positive
repeat rate. Exact traveling-profile certificates give positive floors
independent of temporal depth, even for constant tapes. The successful
instance certificates above remain valid. Other widths, separated bags,
and different projection schedules are outside the new obstruction; the
original counting inequality and mortality remain open.
