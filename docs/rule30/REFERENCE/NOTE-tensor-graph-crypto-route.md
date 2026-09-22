# Tensor networks, De Bruijn graphs, and cryptanalysis: exact scope

Date: 2026-09-13. This follow-up identifies a concrete use of tensor networks
for the fully guarded counting problem. It does **not** prove the cumulative
counting inequality, a positive repeat information rate, auxiliary mortality,
or period-two exclusion. The three proposed subjects do not supply those
conclusions merely by measuring complexity or entropy.

## 1. Tensor networks: represent the correct object

There are three different objects:

1. A single deterministic row, represented as its delta probability
   distribution, is a product state of bond dimension one.
2. The full evolution operator on all input configurations can have large
   operator bond dimension.
3. Our backward message `h_b = T_n^b g_alpha` counts completions to one exact
   guarded history. This is the relevant object for original ancestor counts.

Merbis and Bakker construct an MPO for the **full evolution operator** with
open boundary conditions and study its operator entanglement numerically.
Their calculations stop at prescribed bond-size or numerical limits. Their
Table 1 places Rule 30 in type II.B: open boundaries eventually impose
stripes, and the observed operator entropy drops after its initial growth.
This is not an all-size exponential lower bound for our guarded messages.
See [their original paper, sections 2–3.2](https://arxiv.org/html/2406.04895v1).

Even an operator bond lower bound is a statement about a specified
representation. It is not automatically a lower bound against arbitrary
prediction algorithms. For example, the additive Rule 90 operator over
binary rows satisfies

```text
F = S + S^(-1),       F^(2^k) = S^(2^k) + S^(-2^k)
```

in characteristic two. A cell at a dyadic time can therefore be obtained
from two initial cells without evaluating all intervening times.

**New exact result.** Our actual history transfer has a nonnegative MPO of
bond dimension **four**, and four is minimal in the stated ordering. The
complete proof, boundary weights, and exact verifier are in
[RESULTS-guarded-history-mpo.md](RESULTS-guarded-history-mpo.md). This operator
keeps the guards in `g_alpha` and counts symbols from the original frontier;
it does not replace them with freely chosen intermediate predecessors.

The report also proves a sufficient local certificate for nonnegative MPS
upper compression. It uses a shared latent state throughout a column and
componentwise rational inequalities. This is the precise property missing
from an uncontrolled SVD approximation.

At fixed original length r, the
[inverse-front factorization](RESULTS-inverse-message-front.md) confines the
nontrivial exact message to a core of at most r temporal pairs plus a pinned
tail. Thus merely increasing tape length does not require unbounded bond
dimension at fixed r. The available dimension bound can still grow
exponentially with r; it is an **upper**, not a lower, bound.

The [window-message obstruction](RESULTS-coupled-message-depth-audit.md)
does not rule out this class. A two-state MPS can impose a global parity
condition that is invisible to every proper local projection. This supplies
a concrete distinction between retaining one common latent state and
optimizing different overlapping windows separately.

## 2. De Bruijn graphs: unrestricted row entropy is already maximal

The ordinary Rule 30 graph has vertices `ab`, edges `ab -> bc`, and output
label `a XOR (b OR c)`. Sutner gives the graph construction and analyzes
Rule 30's surjectivity in
[his original paper](https://content.wolfram.com/sites/13/2018/02/05-1-3.pdf).

There is an elementary exact count: every prescribed length-m output word
has precisely four length-(m+2) input words. Choose the two rightmost input
bits freely. Then reconstruct the remaining bits from right to left using

```text
a = output XOR (b OR c).
```

This proves that the unrestricted one-step output language is the full
binary language, with spatial word entropy `log(2)`. It does not compute or
identify every other notion of dynamical or trace entropy. In particular,
the all-zero and spatially alternating fixed configurations remain present.
Maximal growth of allowed row words therefore cannot exclude their constant
columns, let alone identify the lone-seed center's asymptotics.

A graph route must retain chronological guards and original ancestry, or
prove a separate theorem transferring its graph property to those objects.
The [exact history-transfer graph](RESULTS-history-transfer-mixing.md)
already does retain them. Increasing an unconstrained De Bruijn window
would discard the difficult part of the problem.

## 3. Cryptanalysis: the needed statistic is a joint guarded fiber

Meier and Staffelbach's attack on a Rule 30 generator uses guesses of
right-hand seed bits, reconstructs a candidate ring seed, and verifies the
observed output. Its advantage uses unequal adjacent-trace fiber weights.
The paper distinguishes its experiments from an entropy model whose
applicability to the CA source is not established. These are relevant
techniques for analyzing fibers, but no uniform bound for our auxiliary
histories follows. See
[the original paper, sections 2–4](https://link.springer.com/content/pdf/10.1007/3-540-46416-6_17.pdf).

Here is an exact algebraic formulation suitable for a correlation attack.
Fix r and alpha, and temporarily totalize the prescribed trajectory: after
each scan append `3-alpha_t`, even if that scan fails its guard. Let

```text
e_(t,u)(w) = terminal_u(w,t) XOR alpha_t,
e_(t,v)(w) = terminal_v(w,t) XOR alpha_t.
```

Then the desired **unconditional** probability under uniform legal original
words is exactly

```text
p_alpha = |C_r(alpha)| / 2^(2r-1)
        = E_w PRODUCT_(t=1..N, xi in {u,v})
                (1 + (-1)^e_(t,xi)(w))/2.
```

Proof: every factor is the indicator of one required terminal bit. If the
first invalid guard occurs, the product is zero regardless of the artificial
continuation. If all factors are one, this is the actual successful
trajectory, with exactly the required births and tape. No artificial
post-crash state is counted as a successful ancestor.

Expanding the product gives a sum of joint Walsh correlations over all
subsets of these residual constraints. Individual biases or pairwise
correlations do not bound that sum without an additional theorem. Likewise,
the exact chain rule

```text
p_alpha = PRODUCT_t |C_r(alpha[:t])| / |C_r(alpha[:t-1])|
```

for a surviving tape still has factors equal to one at the known repeats
in the 36-ancestor plateau. A valid information bound must account for the
whole history.

## 4. The next decisive test

The concrete candidate class is now nonnegative MPS upper messages with
the local simulation certificates in the new report. A proposed compression
must pass two different tests:

1. Its rational local inequalities must majorize the **whole** guarded
   message, including both legal origin evaluations.
2. Its evaluated probability must meet a specified repeat bound on the
   saved plateau histories. A valid but excessively loose majorant fails
   this test.

We executed a bounded first test on `alpha=0^22`, r=41, where the
width-three scheme is known to fail. Exact proportional-suffix merging
stopped at its declared bond cap after eleven of forty required transfers.
Its valid continuation bound is `|C_41(0^22)| <= 64,435*2^60`, compared with
the required `2^60`. The method preserves only mixtures of point-mass
suffixes; this tests a narrow subclass, not general MPS compression. See
[the exact result and verifier](RESULTS-guarded-history-mpo.md#10-a-bounded-exact-compression-attempt-on-the-width-three-obstruction).

Thus neither a successful compressed certificate for this discriminator nor
an all-r/all-alpha family was obtained. The required advance remains a
useful certified compression or another cumulative information bound.
Tensor-network rank growth, graph entropy, and apparent cryptographic
mixing alone would not establish it.

**Follow-up:** the [independent guarded UNSAT proof](RESULTS-constant-zero-history-certificate.md)
resolves the particular test case exactly: `C_41(0^22)=empty`. This is a
finite count certificate obtained outside the stalled MPS computation; it
does not establish the unrestricted counting inequality.
