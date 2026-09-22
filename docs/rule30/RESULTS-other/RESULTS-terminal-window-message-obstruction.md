# A single terminal-window upper message eventually becomes trivial

Date: 2026-09-13. **An all-length obstruction to one compressed message
family, not a refutation of the counting conjecture.**

Retain the original high bit A_0 and the final k temporal pairs of the exact
column graph, maximizing over every earlier pair after each spatial transfer.
If at least three temporal pairs were forgotten, this certified upper message
becomes identically one whenever

```text
r-1 >= 2*(4^k-1).
```

Its resulting original-ancestor count bound is then the entire legal universe,
`2^(2r-1)`, independently of the prescribed tape. Thus a fixed-width terminal
window of this type cannot prove any uniform positive rate in repeats.

This theorem concerns a **single** window. It does not exclude the minimum
of overlapping bag messages that jointly retain all terminal guards. It is
also different from the stationary-superharmonic obstruction: the messages
here may depend on the spatial horizon and are propagated at every step.
Unrestricted counting, mortality, and period-two exclusion remain open.

## 1. Exact object and certified relaxation

Fix a chronological tape alpha of length n. The
[exact column graph](RESULTS-cumulative-history-transfer.md) has states

```text
q = (A_0,A_1,B_1,...,A_n,B_n).
```

Its transition delta(q,x), for original symbol x in {0,1,2,3}, retains all
bulk layers. The tape's complete chronological guards specify the terminal
indicator g_alpha, supported on its two column signatures, with A_0 free.
Write

```text
(P f)(q) = (1/4) SUM_x f(delta(q,x)).
```

For original length r the exact successful-tape probability is the average
of `P^(r-1) g_alpha` at the two legal origin columns. Only original input
symbols carry these probability factors.

Put m=n-k and retain the projection

```text
pi(q) = (A_0,A_(m+1),B_(m+1),...,A_n,B_n).
```

Define the pointwise upper projection

```text
(E f)(q) = max { f(z) : pi(z)=pi(q) }.
```

The canonical relaxed messages are

```text
H_0 = E g_alpha,       H_(ell+1) = E P H_ell.
```

Monotonicity and E f>=f prove `H_ell >= P^ell g_alpha`, so this is a valid
upper certificate. Also `0<=H_ell<=1`. At the leaf, H_0 is exactly the
indicator that the retained k pairs equal their target signature: the other
n-k terminal guard pairs have been maximized away.

## 2. Three hidden layers provide constant effective inputs

For fixed incoming original A_0, summarize the hidden layers by a channel

```text
(p,F),       F:{0,1,2,3} -> {0,1,2,3}.
```

Here p is the final old high bit of the hidden block, and F maps each possible
original input symbol to the new pair entering the retained block. Initially
`(p,F)=(A_0,identity)`. Choosing the next old temporal pair (u,v) replaces it by

```text
p' = u,
F'(x) = 2*(u XOR (v' OR a)) + v',
v' = v XOR (p OR b),       (a,b) = bits of F(x).
```

There are only `2*4^4=512` possible channel types. The complete finite
calculation gives:

| Original A_0 | Channel counts after 0,1,2,3,4 hidden layers |
|---:|---|
| 0 | 1,4,14,22,22 |
| 1 | 1,4,10,10,10 |

The sets at depths three and four are equal in both sectors, so induction
proves stabilization for every greater hidden depth. More specifically,
both sectors contain these six constant channels:

```text
(p, constant entering symbol):
(0,0), (0,2), (0,3), (1,0), (1,1), (1,2).
```

The verifier provides a three-layer old-column witness for every channel
in each A_0 sector. The six constant types also reproduce exactly themselves
under all four choices of the next old pair. These are complete local finite
certificates, not an extrapolation from large original frontiers.

The two apparently missing boundary controls introduce no restriction.
When the entering symbol has low bit one, its first OR masks p. Therefore
the controls `(0,1)` and `(1,1)` have identical action on all retained pairs,
as do `(0,3)` and `(1,3)`. This holds for every k: equality after the first
retained layer propagates through the remaining identical cascade.

Thus, after at least three hidden layers, the max projection can supply
**any effective boundary control**, independently of which original symbol
was averaged in P. Both possible new original high bits still occur; the
same controllability is available again in either sector at the next step.

## 3. Uniform saturation theorem

Form a directed graph on the `4^k` retained-pair tuples. From each tuple allow
every old boundary high p and every entering symbol c. This graph contains
the projection of every edge of T_k, because the exact column graph uses
these same controls with an additional original-high coordinate.

The [all-depth connectivity theorem](RESULTS-history-transfer-mixing.md)
therefore makes this projected graph strongly connected. Its zero tuple has
a self-loop, using p=0,c=0. Every vertex reaches zero in at most `4^k-1`
edges, and zero reaches every target within the same bound. Waiting at zero
shows that every vertex reaches every target in **every exact length**

```text
ell >= 2*(4^k-1).
```

Choose such a path to the target retained signature. At each edge, section 2
supplies a constant hidden channel implementing its control for all four
original symbols. Hence all branches of that averaged step have the same
next retained-pair tuple. The original-high bit can vary, but the next path
edge remains available in both sectors. Induction along the path gives value
one at its beginning. Since H_ell<=1 already,

```text
H_ell(q) = 1 for every q,
whenever m>=3 and ell>=2*(4^k-1).
```

Evaluating at either legal origin and setting ell=r-1 gives the stated
trivial original count bound. The hidden choices are reselected by the upper
projection at successive spatial steps; they need not form one actual
original history. That freedom is legitimate for an upper relaxation, and
it is precisely what destroys the useful bound here.

The failure is not confined to tapes with no ancestors. For alpha=0^n,
D=n-1, and the existing graph connectivity and zero self-loop ensure that
C_r(alpha) is nonempty for all sufficiently large r. Such r can also exceed
the saturation threshold. For any fixed c,epsilon>0, choose n with
`c*2^(-epsilon*(n-1))<1`. This message then returns one on a nonempty actual
history class when the desired certified upper probability would be smaller.

## 4. Bounded independent checks and remaining scope

The [exact verifier](../../experiments/rule30/terminal_window_message_certificate.py)
and [artifact](../../experiments/rule30/terminal-window-message-certificate.json)
check the channel closure, all twelve three-layer constant-channel witnesses,
and the OR-masking identity. They construct the exact compressed max-sum
operator and check every terminal target for k=1,2,3:

| Retained pairs k | Compressed states | Worst exact saturation time |
|---:|---:|---:|
| 1 | 8 | 2 |
| 2 | 32 | 5 |
| 3 | 128 | 8 |

For k=1,2 a separate full-column implementation maximizes directly over all
forgotten assignments at total depths four and five, and agrees with every
compressed transition and checked message update. Counts remain integers;
normalization is the exact denominator `4^ell`. The small-case times sharpen
the general bound for those widths only; no formula is inferred from them.

Run:

```text
uv run --no-project python experiments/rule30/terminal_window_message_certificate.py
```

The saved run completed in under one second with a 15-second cap. It checks
finite local/channel objects and temporal columns, not the original-frontier
census. No frozen-oracle change, model training, GPU, or paid compute was used.
The theorem leaves open coupled overlapping messages, growing separators,
and other upper certificates that retain the discarded guard correlations.
