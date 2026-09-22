# Sparse finite origins: exact coherent-output minima and a two-one theorem

This investigation asks how few initial ones can generate a maximally
coherent positive half-row. It gives exact finite minima through time 53
and an all-time classification for origins with at most two ones. It does
not prove the lone-seed quarter-wave bound, a global mass-energy bound, or
P1/P2/P3.

## 1. The exact optimization problem

Let the initial row have finite support in the nonpositive half-line,
with its rightmost one at zero. For n=1 modulo 4, call its positive output
fully coherent when

\[
x_i^{(n)}=\begin{cases}1,&i\equiv1\pmod4,\\
                       0,&i\equiv3\pmod4,
        \end{cases}\qquad 1\le i\le n,\quad i\text{ odd}.
\]

Even positive sites are unrestricted. This is exactly the condition

\[
P_n=\sum_{m\ge0}(x_{4m+1}^{(n)}-x_{4m+3}^{(n)})=(n+3)/4.
\]

Define M(n) to be the minimum initial Hamming weight among such rows.
Initial sites i<1-n cannot influence any positive site by time n, so
removing them does not affect this optimization. It suffices to consider
initial support in [1-n,0].

In right-front coordinates E_j(t)=x_(t-j)^(t), the prefix map is

\[
(R E)_j=E_j\oplus(E_{j-1}\lor E_{j-2}),\qquad E_{-1}=E_{-2}=0.
\]

Its inverse determines each successive bit from the two already recovered
bits. Thus R^n is a bijection on prefixes of length n. Coherence prescribes
the even output depths: b_j=1 for j=0 modulo 4 and b_j=0 for j=2 modulo 4.
The n//2 odd output depths are free. Exhausting their 2^(n//2) completions
and inverting each gives the exact minimum, not a stochastic search or a
relaxation of realizability.

The implementation packs all completions into independent bits of Python
integers. Each XOR/OR inverse gate operates on all completions at once.
Bit-sliced binary addition then counts initial ones for every completion.
This is an exact parallel evaluation of the complete finite search space.

## 2. Finite minima

| n | Output completions exhausted | M(n) | Number attaining M(n) |
|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 |
| 5 | 4 | 2 | 1 |
| 9 | 16 | 2 | 1 |
| 13 | 64 | 3 | 1 |
| 17 | 256 | 3 | 1 |
| 21 | 1,024 | 5 | 2 |
| 25 | 4,096 | 5 | 1 |
| 29 | 16,384 | 7 | 9 |
| 33 | 65,536 | 7 | 10 |
| 37 | 262,144 | 6 | 1 |
| 41 | 1,048,576 | 6 | 1 |
| 45 | 4,194,304 | 7 | 1 |
| 49 | 16,777,216 | 9 | 8 |
| 53 | 67,108,864 | 9 | 3 |

The total is 89,478,485 output completions. The values are not monotone.
For example, six initial ones suffice at n=41, whereas seven are necessary
at n=33. There is no extrapolation to larger n.

The initial row with ones at -2 and 0 (word `101`) attains full coherence
at both n=5 and n=9. Three-one examples attain it at n=13 and n=17.
The JSON records explicit minimizing initial words and independent forward
checks for every table entry.

No counterexample to `P_t^2<=C t M_initial` was found in this restricted
search. That is not positive evidence for a particular global constant:
the search concerns only maximally coherent outputs at the listed times,
not all outputs, times, or initial rows.

## 3. All-time classification for at most two initial ones

The following is not an extrapolation from the table:

\[
\boxed{\text{With at most two initial ones, full coherence at }
       n\equiv1\pmod4\text{ is possible exactly at }n=1,5,9.}
\]

First, E_0(t)=1 for every t. Therefore the depth-two recurrence simplifies
to E_2(t+1)=E_2(t) XOR 1, irrespective of depth one, giving

\[
E_2(t)=E_2(0)\oplus(t\bmod2).
\]

For n>=5 with n=1 modulo 4, coherence requires E_2(n)=0. Hence E_2(0)=1.
Together with E_0(0)=1 and the mass bound, this forces the entire initial
row to be exactly `101`, with all remaining initial cells zero. In
particular, the actual lone seed cannot attain full coherence at any
such n.

Now consider the closed right-front prefix of length 16 for that initial
row. In integer encoding with depth j stored in bit j, the transition is

\[
R_{16}(u)=(u\oplus((u\ll1)\lor(u\ll2)))\ \&\ (2^{16}-1).
\]

Starting at u=5, it returns exactly after 64 steps:
R_16^64(5)=5. This is a verified finite cycle of a closed subsystem;
therefore its repetitions describe the actual prefix for all time.
At each possible phase n=1 modulo 4, the following even depth disagrees
with the coherent target:

| n modulo 64 | 1 | 5 | 9 | 13 | 17 | 21 | 25 | 29 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| mismatching depth | 8 | 6 | 14 | 6 | 8 | 6 | 10 | 6 |

| n modulo 64 | 33 | 37 | 41 | 45 | 49 | 53 | 57 | 61 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| mismatching depth | 8 | 6 | 12 | 6 | 8 | 6 | 10 | 6 |

All these depths are below 16. Consequently every n>=17 in the required
time class fails coherence. At n=13 the depth-six mismatch already lies
inside the positive observation interval. Direct evaluation gives
coherence at n=1,5,9, completing the classification.

The finite certificate stores all 64 states and the phase witnesses. Its
force for arbitrarily large time comes from exact return to the initial
state in a closed prefix, not from merely observing failure at 64 times.

In particular, M(n)>=3 for every n>=13 in the time class under study.
This is a constant lower bound, not a proof that M(n) grows with n.

## 4. A precise conjectural mass-growth target

The finite table suggests the falsifiable inequality

\[
\boxed{n\le8M(n)-7,\quad\text{equivalently}\quad
       P_n\le2M(n)-1\text{ for fully coherent outputs}.}
\]

It holds in every listed finite case. Section 3 proves it for initial
mass at most two. It is unproved in general. The current argument does
not extend automatically when another initial one is permitted: that
one changes the closed-prefix orbit, and a uniform avoidance argument
has not been supplied.

Even a proof of this inequality would concern perfect phase coherence.
It would not control rows with substantial but imperfect phase imbalance,
and would not imply P_t=o(t). A useful extension would need quantitative
control of how many prescribed odd sites may fail, retaining the actual
initial configuration rather than averaging over an ensemble.

## 5. Reproduction and verification

Run the [standalone script](../../experiments/rule30/quarter-wave-phase/sparse_coherent_origins.py):

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  experiments/rule30/quarter-wave-phase/sparse_coherent_origins.py \
  --output experiments/rule30/quarter-wave-phase/sparse-coherent-origins.json
```

The [JSON record](../../experiments/rule30/quarter-wave-phase/sparse-coherent-origins.json)
contains all finite minima, minimizing examples, and the all-time two-one
certificate. Direct scalar enumeration independently checks the first
four minimization problems, through n=13. A physical-coordinate set
implementation of Rule 30 independently verifies each minimizing example.
The periodic-prefix certificate checks every transition and every phase
rejection with exact integer arithmetic.

The search space and memory use grow exponentially with n. The default
stops at n=53. The existing quarter-wave current and seed audit artifacts
are not modified by this experiment.
