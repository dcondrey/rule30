# Fixed contiguous windows through width three cannot give a repeat rate

Date: 2026-09-13. **An all-length obstruction to the specified compressed
certificate family. The original counting inequality is not refuted.**
Finite-frontier mortality and period-two center exclusion remain open.

The preceding [message experiments](RESULTS-guarded-message-certificates.md)
showed that coupled windows and exact treatment of the original boundary
can certify saved examples. This continuation addresses whether those
certificates can scale to arbitrarily long histories. They cannot when
restricted to all contiguous windows of width one, two, or three, with
projection after each spatial transfer. The failure already occurs on
constant scalar tapes; switches are not needed to expose it.

## 1. Exact statement and scope

Fix the chronological tape alpha=0^n. Let g_alpha be its complete guarded
column indicator, let P average the four original-symbol transitions, and
let C_k be the minimum of max projections onto **every** bag consisting
of A_0 and k consecutive temporal pairs. Define normalized messages

```
H_0 = g_alpha,       H_(ell+1) = C_k P H_ell.
```

The desired probability is at most the mean of H_(r-1) at the two legal
origin columns. Original length r remains fixed within this count. The
signature includes every chronological guard and birth; this is not an
ensemble of fresh current predecessors.

**Theorem.** These message lower bounds hold at every temporal depth in
the indicated ranges:

| Window width k | Temporal depth | Global normalized floor | A sufficient spatial horizon ell |
|---:|---:|---:|---|
| 1 | n>=3 | 5/64 | ell>=n |
| 2 | n>=7 | 4^(-6) | ell>=11+5*ceil((n-6)/3) |
| 3 | n>=11 | 4^(-10) | ell>=15+5*ceil((n-7)/3) |

"Global floor" means H_ell(q) is at least that constant at **every**
column q, and remains so for every later ell. The width-one proof is given
in the [singleton wave report](RESULTS-singleton-message-wave.md). The
width-two and width-three proof is below.

Consequently none of these three certificate families can establish

```
|C_r(alpha)| / 2^(2r-1) <= c * 2^(-epsilon*D(alpha))
```

uniformly for any c,epsilon>0. Choose n so that its right side, with
D=n-1, is smaller than the corresponding floor, and choose original r
beyond the displayed horizon. Spatial mixing permits such r to be chosen
with a nonempty actual ancestor class. The true probability tends to
4^(-n) as r grows; the positive floor belongs to the **upper relaxation**.

For example, width three cannot certify the one-bit target for 0^22 at
any r>=41: its upper probability is at least 2^(-20), whereas the target
is 2^(-21). This is a failure of that certificate, not a counterexample to
the true one-bit inequality.

An exact final origin block of b transfers does not remove the floor once
r-1-b exceeds the stated horizon. In particular, any fixed bound on b
leaves the obstruction intact. Grouped transfers throughout the calculation,
different or separated bags, widths beyond three, and other representations
are not excluded by this theorem. No claim about all bounded-width message
families is made.

## 2. A Boolean lower certificate for a numerical upper message

For a Boolean support f define the robust operator

```
R_k f = C_k [MIN_(x=0..3) f(delta(q,x))].
```

Every column contributing inside that minimum must work for all four input
symbols with the **same** old temporal column. Since a minimum is at most
an average,

```
R_k f <= C_k P f.
```

Suppose H_B>=c*f. Monotonicity and positive homogeneity imply

```
H_(B+t) >= c * R_k^t f.
```

Thus a support that becomes universal under R yields a permanent numerical
floor without another loss of amplitude. This is a lower certificate for
the values of an upper-count algorithm; it is not a lower ancestor bound.

The support of the integer message after B steps is computed exactly by
replacing each four-term sum by an existential Boolean predecessor and
then taking the same bag projections. Every positive integer is at least
one, so the normalized numerical message is at least 4^(-B) on that
support. No independence assumption enters this statement.

## 3. Finite seed cores lift to all depths

Take (k,B)=(2,6) or (3,10). The
[inverse-message front theorem](RESULTS-inverse-message-front.md) proves
that after B spatial transfers the entire message factors into a depth
B+1 core and deterministic pins on the remaining temporal tail. This
factorization also applies to the canonical contiguous-window messages.

The [seed verifier](../../experiments/rule30/message_wave_seed.py) computes
the Boolean core at depth seven or eleven, respectively. It then checks
the **entire memory** of B stacked canonical inverse scans at two cuts
separated by two temporal layers. Those memories coincide, with the same
alternating input phase. Their subsequent output is therefore `3,0,3,0,...`
for every greater depth by induction.

The last core bag already pins its complete window. Each added overlapping
pin bag imposes exactly the next new tail pin. This verifies the interface
seam as well as the periodic tail; matching only a finite core would not
have sufficed.

Let S_(k,n) be the resulting full-depth seed support. We have therefore
proved, at every n>=B+1,

```
H_B >= 4^(-B) * 1_(S_(k,n)).
```

The complete core masks, inverse-memory return, and seam checks are retained
in [message-wave-seed.json](../../experiments/rule30/message-wave-seed.json).

## 4. Five robust steps advance the interface by three bags

A bag table is represented by its exact bit mask: bit

```
A_0 + 2*(z_1 + 4*z_2 + ... + 4^(k-1)*z_k)
```

indicates whether that assignment is allowed. Write U for the universal
mask. Each seed support is a minimum of bags whose masks form

```
U U [a finite interface] [two alternating pin masks ...].
```

The number of bags is m=n-k+1; the displayed infinite profile is cropped
after exactly m masks. This describes a fixed original-count separator,
not a temporally periodic frontier.

Five robust transitions take the seed profile to one with five leading
U masks. Thereafter five phases repeat, increasing the number of leading
U masks by three each cycle. The prefix increments in the five stable
phases are

```
width two:   (1,0,0,1,1),
width three: (1,1,0,1,0).
```

For example, the width-two first interface is

```
ff0ff00f, 00000ff0, 0f000000,
```

followed by the alternating pin masks `000000c0,03000000`. The masks encode
the adjacent constraints that singleton bags lose. Wider bags delay their
loss here, but do not stop the advancing relaxed interface. All width-three
masks and intermediate phases are saved exactly in the propagation artifact.

The asserted transitions are **inclusions of supports**. Exact equality
with the canonical numerical messages is not required. Starting from the
proved seed lower bound, each inclusion preserves its numerical amplitude.

After at most

```
5 + 5*ceil(max(0,m-5)/3)
```

robust steps, the universal prefix covers all m bags, so the support is the
entire column space. Adding B gives the theorem's horizons. These are
sufficient bounds, not claims of optimality.

## 5. Why the propagation check proves all lengths

The masks were suggested by finite depth-32 calculations. The
[regular-profile verifier](../../experiments/rule30/regular_message_wave.py)
checks the resulting proposed transitions at **all** prefix and tail lengths
by closing finite automata. Its proof obligation is as follows.

For each desired output bag assignment, there must exist an old column
with that assignment whose four successors satisfy every input-profile bag.
Different marked assignments may use different witness columns, as permitted
by max projection. The four input branches for one marked assignment share
one witness throughout the temporal scan.

A finite context contains the shared old window and the four branch states.
An edge reads one old pair, computes all four transformed windows, and is
allowed precisely when all four satisfy the current input mask. The first
k-1 old pairs provide the warmup before a whole bag exists.

A second finite automaton generates paired input/output mask profiles:
the required universal prefix, its optional arbitrary-length continuation,
the finite interface, and a periodic tail. Every state may terminate because
the claim covers all common-length finite crops of extendible infinite
profiles. Input and output masks are cropped at the same bag index.

Exactly one bag position is marked. At that step the edge is restricted to
the requested old window assignment. A subset construction retains every
context still capable of witnessing that request. Subsequent edges continue
the **same** witness path. Distinct subsets are kept separate; they are not
unioned across different profile prefixes or marked assignments.

An empty witness subset after a permitted mark would refute this maskwise
inclusion certificate. Complete reachability closure with no such subset
proves it for every generated finite length. This requirement is stronger
than necessary when a desired local assignment is globally inconsistent,
but a completed no-empty certificate remains sufficient.

The finite closure passes for both original A_0 sectors, both widths, five
initial transitions and five stable transitions: forty product certificates.
They contain 16,828 reachable product vertices and 29,076 labeled edges;
the largest individual product has 932 vertices. Every marked reachable
subset is nonempty. The complete propagation check took under one second.
The stable transitions include every universal-prefix length a>=5 and every
finite crop. There is no extrapolation from a maximum tested n in this step.

## 6. Computation and the remaining research problem

The supporting [channel DP](../../experiments/rule30/message_channel_dp.py)
computes exact existential and robust Boolean projections by scanning
temporal layers. It does not allocate a column array of size 2*4^n. A
numeric Pareto implementation is also provided for exact upper-message
queries; the all-length wave proof uses the Boolean version.

The [channel artifact](../../experiments/rule30/message-channel-dp.json)
records comparisons with dense controls through depth six, and the finite
depth-16/depth-32 profiles used to propose the waves. The dense controls
compare 344 numeric and 5,136 Boolean table entries. Those finite observations
have a different status from the subsequently proved regular-profile closure.

A separate [cropped-profile check](../../experiments/rule30/regular_message_wave_independent.py)
compares eighty selected finite crops against the channel DP, independently
of the product-subset closure implementation. All 440 bag-mask inclusion
comparisons pass. This checks the new automaton's interpretation; the finite
closure proof supplies its all-length scope.

Reproduce the new proof components with:

```
uv run --no-project python experiments/rule30/message_wave_seed.py
uv run --no-project python experiments/rule30/regular_message_wave.py
```

The propagation proof and its full masks are retained in
[regular-message-wave.json](../../experiments/rule30/regular-message-wave.json).
The inverse-front and singleton results have their own linked exact verifiers.
All computations are local, bounded, and integer or Boolean. Existing frontier
censuses, GPU work, paid compute, and the frozen oracle were not rerun or changed.

This closes the proposed scaling hypothesis for the tested contiguous
windows through width three. Their pointwise least locally certified
messages already fail, so choosing different numerical weights inside those
same stepwise classes cannot repair them. Correlations must be retained in
a different way, or a different certificate schedule must be justified.

The true cumulative-counting question is unchanged: no unrestricted uniform
positive-rate upper bound on actual original ancestors has been proved, and
no counterexample to the one-bit inequality has been found. The new obstruction identifies a
specific loss of common-history consistency inside the relaxation. It does
not establish a repeat budget, mortality, or any new center-period exclusion.
