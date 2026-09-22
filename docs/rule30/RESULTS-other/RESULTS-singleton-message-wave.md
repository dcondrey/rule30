# Singleton minimum messages have a positive floor at every temporal depth

Date: 2026-09-13. **An all-depth obstruction to the canonical singleton
message class is proved.** It does not refute the counting inequality or
exclude wider bags. Mortality and period-two exclusion remain open.

For the chronological tape alpha=0^n, n>=3, let H_ell be the normalized
canonical upper message using the minimum of all singleton temporal-pair
bags, each also retaining A_0. Then

```text
H_ell(q) >= 5/64 for every column q and every ell>=n.
```

Thus its original-root upper probability is at least 5/64 whenever r-1>=n,
although the required positive-rate bound tends to zero as D=n-1 grows.
This strengthens the previously observed fixed-depth floors to an obstruction
uniform in temporal depth. The proof is a finite base followed by an exact
moving-interface identity, not an extrapolation from those observations.

All probabilities count legal **original** auxiliary frontiers with the
prescribed chronological guards. The result diagnoses a relaxation of those
counts; it is not an assertion about singleton-seed frontiers.

## 1. Message and moving-cylinder definitions

Use the exact column coordinates

```text
q = (A_0,z_1,...,z_n),       z_j=2A_j+B_j.
```

Let P average the four actual original-symbol transitions. Let C be the
minimum, over j=1,...,n, of the maximum over columns agreeing on (A_0,z_j).
The [canonical message theorem](RESULTS-guarded-message-certificates.md)
gives

```text
H_0=g_(0^n),       H_(ell+1)=C P H_ell.
```

For 1<=d<=n define the indicator F_d by:

* pairs 1 through d and A_0 are unrestricted;
* if pair d+1 exists, its high bit is zero;
* pairs d+2,d+3,... are respectively `3,0,3,0,...`.

In particular F_n is identically one. The crucial statement is

```text
C P F_d >= F_(d+1),       for every 3<=d<n.             (1)
```

There is no loss of normalized amplitude when this interface advances.

## 2. All-length proof of the interface identity

It is enough to prove the stronger Boolean assertion

```text
C [MIN_x F_d(delta(q,x))] >= F_(d+1).                  (2)
```

For every singleton assignment occurring in F_(d+1), we construct a complete
column with that assignment whose **four** original-symbol successors all
belong to F_d. This proves every required max-projection is one. It retains
one common hidden column for all four symbols; no separate maximizer is used
inside the original-symbol average.

At a cut through layer d write

```text
p=A_d,       u=A'_d,       v=B'_d.
```

The local rule implies

```text
u = p XOR (v OR A'_(d-1)).
```

Consequently if p=0 the new pair cannot be `1`, and if p=1 it cannot be `3`.
Choose the next old pair to be `3-p`. Its new high bit is always zero:
for p=1 its new low is one; for p=0 the preceding displayed relation makes
`(1-v) OR u=1`. Choosing the following old pair to be `0` then emits `3`.
The old tail `3,0,3,0,...` subsequently emits `0,3,0,3,...` by a two-state
local calculation. These identities hold simultaneously for all four
original input symbols.

This construction handles a pinned singleton in layers 1,...,d: fill the
first d pairs arbitrarily while retaining the pin, then use the displayed
interface and tail. It also handles any pinned singleton strictly after
d+2, because the pin then already has the required tail value.

Two interface cases remain. The
[constant-channel theorem](RESULTS-terminal-window-message-obstruction.md)
supplies, through any d>=3 earlier layers and in either A_0 sector, a
constant effective entering pair c with old boundary high p for each of

```text
(p,c) = (0,0), (1,0), (0,2).
```

The same channel works for all four original symbols.

If pair d+1 is pinned to `2A+B`, choose

| Pinned high A | Constant boundary (p,c) | Old pair d+2, if present |
|---:|---|---:|
| 0 | (B,0) | 1 |
| 1 | (0,2) | 0 |

The new high at d+1 is zero, and the next new pair is `3`. Append the
alternating old tail as before. This works for all four possible pinned
symbols.

If pair d+2 is pinned, it is either `0` or `1`. Set A=1 minus that pinned
symbol, choose boundary `(p,c)=(0,2A)`, and set old pair d+1 to `2A`.
Again the new high at d+1 is zero and the new pair at d+2 is `3`.

These cases exhaust all singleton positions, including when the interface
reaches the last pair. They prove (2), and hence (1), for every depth.
The adjacent relation used in this construction can be discarded by a
singleton projection. A bag retaining both interface pairs can retain that
relation, so the proof does not extend automatically to width two.

## 3. A finite base proves the uniform floor

For a constant-zero tape, the complete guarded signature has temporal pairs

```text
0,3,0,3,... .
```

This follows directly by induction in the signature construction: the
transported birth suffix is alternating and ends in `3`, and the required
incoming bulk pair alternates between `0` and `3` to finish each scan with
scalar zero.

The [inverse-message front theorem](RESULTS-inverse-message-front.md)
applies to the canonical contiguous-window minimum messages as well as to
exact counts. For three spatial transfers and n>=4 it factors H_3 into
its depth-four singleton core and a deterministically pinned tail. Three
canonical inverse scans of `0,3,0,3,...` give the representative

```text
0,1,3,0,3,0,3,0,... .
```

The inverse transducer returns to the same complete three-scan memory at
layers four and six. That finite return proves the alternating continuation
at every greater depth. Thus its fixed tail begins at layer five with
`3,0,3,0,...`, and the core's fourth high bit is zero.

The exact depth-four calculation gives

```text
H_3(q) >= 5/64 on every depth-four column with A_4=0.
```

The separate depth-three calculation gives the same lower bound on every
column. Therefore, at every n>=3,

```text
H_3 >= (5/64) F_3.
```

Monotonicity and positive homogeneity of C and P, followed by (1), give

```text
H_d >= (5/64) F_d,       3<=d<=n.
```

Since F_n=1, the desired global floor follows at step n. Both operators
preserve constant functions, so it persists for every later spatial step.

## 4. Consequence and limits

At the original boundary the upper probability is the mean of H_(r-1) at
the two legal origin columns. It is therefore at least 5/64 for r>=n+1.
An exact original-boundary block of b steps does not remove the floor once
the preceding compressed horizon r-1-b is at least n: averaging a function
already bounded below by a constant preserves that lower bound.

For any c,epsilon>0, choose n with

```text
c*2^(-epsilon*(n-1)) < 5/64.
```

At sufficiently large original lengths the canonical singleton certificate
then misses the target. These may be chosen as nonempty actual history
classes: the established spatial mixing theorem gives positive probability
to every prescribed finite tape at all sufficiently large r. The true
probability tends to `4^(-n)`; it is the upper relaxation that has the
constant floor.

This rules out a uniform positive repeat rate for **all singleton bags with
projection after every spatial step**, even though their minimum preserves
every guard at the initial leaf. It does not exclude wider or separated
bags, a different projection schedule, grouped exact transfers throughout
the computation, or a different message representation. The active counting
inequality itself remains unproved and unrefuted.

## 5. Exact verifier

Run:

```text
uv run --no-project python experiments/rule30/singleton_message_wave.py
```

The [verifier](../../experiments/rule30/singleton_message_wave.py) and
[artifact](../../experiments/rule30/singleton-message-wave.json) retain:

* the complete three-step depth-three and depth-four singleton tables;
* the periodic return of the three inverse-scan memories;
* the six physical-cut reset identities and four arbitrary-interface cases;
* the previously certified all-length constant-channel closure;
* 700 explicit singleton completion witnesses, each checked under all four
  original inputs by a full-column implementation.

The saved run completed in under one second with a 15-second cap. The
all-depth conclusion rests on the interface construction and proved inverse
factorization. No frontier census, model training, paid compute, GPU work,
or frozen-oracle modification was used.
