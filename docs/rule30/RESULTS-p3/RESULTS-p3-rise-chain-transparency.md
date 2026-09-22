# A rising edge certifies an exact two-time pause

Date: 2026-09-14. **At every non-origin site, a rising edge in the
intermediate low field makes two B steps, or two C steps, preserve the
old high bit. Consecutive such guards certify an arbitrarily long
two-time chain from a word in the preceding spatial column.**

This strengthens the [last-rise transport rule](RESULTS-p3-two-time-rise-reset.md)
at an actual intermediate rise: the old high bit itself is the answer,
so no Gray-field range parity is needed there. The certificate below is
exact, but constructing its actual predecessor word and obtaining the
earlier endpoint remain charged. No shrinking-work recurrence for P3 is
proved.

## 1. One guard suffices

Digits are low-first: input digit i is D_i+2H_i and output digit i is
P_i+2Q_i. Additions below are in F2; OR is Boolean OR. The
[bitplane equations](RESULTS-p3-two-affine-scans.md) are

```
P_i = D_i + (P_(i-1) OR Q_(i-1)),
Q_i = H_i + (Q_(i-1) OR D_i).                    (1)
```

B uses virtual output (P_-1,Q_-1)=(1,0), and C uses (0,1).
Fix either generator g, use it at both times, and write

```
A=low(gY), Cmid=high(gY), q=high(g²Y).
```

For i>=1, assume the single intermediate guard

```
A_(i-1)=0, A_i=1.                               (2)
```

The first equation in (1) then gives
Cmid_(i-1)=1+D_i. Consequently

```
Cmid_i = H_i + ((1+D_i) OR D_i) = H_i+1,
q_i = Cmid_i + (q_(i-1) OR 1) = H_i.            (3)
```

This proves the all-input, all-tail identity. It requires no earlier
rise and no condition on the final incoming high carry. At the origin
the boundary is different: B² adds2 modulo4 to the root digit, so its
high bit flips; C² fixes the root digit, so its high bit is unchanged.
Thus (3) applies only at i>=1 for B, while the C origin is transparent
without a guard.

For actual center queries, the already proved
[high-bit realizations](RESULTS-p3-actual-b-query.md) are, for h>=1,

```
c_(2h)   = high(digit_(h-1)(C^(h+1)(0))),
c_(2h+1) = high(digit_(h-1)(B^(h+2)(0))).
```

An appropriate guard chain can therefore move either requested high bit
backward by pairs of time steps at the same spatial site. This is a
conditional query reduction, not a claim that the required guards occur.

## 2. A complete predecessor-word certificate

Fix i>=1 in an actual trajectory Y_s=g^s(Y_0). Let d_s and h_s be
the low and high bits at i. Write w_s for the digit at i-1 at time s,
p(w)=w mod2, and O(w)=1[w!=0]. The output-time indexing in (1) gives

```
d_s = d_(s-1) + O(w_s).                         (4)
```

Suppose the earlier endpoint is time a and the first middle time is
tau=a+1. The first guard holds exactly when

```
p(w_tau)=0,  d_a + O(w_tau)=1.                  (5)
```

After this guard d_tau=1. For the next guard, at time tau+2, the
necessary and sufficient conditions are

```
p(w_(tau+2))=0,
O(w_(tau+1))=O(w_(tau+2)).                       (6)
```

Thus the pair consisting of the intervening digit and the next checked
digit belongs to the four-pair language

```
(0,0), (1,2), (2,2), (3,2).                    (7)
```

Induction proves the complete certificate: (5), followed by (7) for
the pairs (w_(tau+2k-1),w_(tau+2k)), k=1,...,K-1, is equivalent to
all K intermediate guards. Equations (2)--(3) then give

```
h_(a+2K)=h_a.                                  (8)
```

For a supplied predecessor word, extending until the first failed pair
finds the maximal chain beginning with the specified first guard.
Checking K guards reads 2K-1 predecessor digits and the entering low
bit d_a; the intermediate high history at site i is unnecessary.

## 3. Retain the actual ancestry of that word

Not every word satisfying (7) is an actual predecessor history. The
three possible digit permutations at an interior site are

```
A: (0,3,2,1), B: (1,2,3,0), C: (3,2,1,0),
```

where each tuple lists outputs on inputs0,1,2,3. The controlling state
is A when the preceding spatial output digit is0, B when it is1, and C
when it is2 or3. No state sends3 to2. Therefore an actual trajectory
reduces (7) to

```
(0,0), (1,2), (2,2).                           (9)
```

At i>=2 this also gives an exact pullback to site i-2, evaluated at the
later, checked time of each pair:

| Predecessor transition | Required second-left output digit |
|---|---|
| 0 to0 | 0 |
| 2 to2 | 0 |
| 1 to2 | any nonzero digit |

These conditions are necessary and sufficient for the displayed
transition when its input digit is fixed. In particular both B and C
send1 to2. At i=1 the controlling state is the fixed generator boundary
instead of an actual second-left column.

There is a further monotonicity constraint: the checked predecessor
digits, all in {0,2}, have the form 0*2*. A checked2 followed at the next
check by0 would require intervening0 by (9), but no A, B, or C sends2
to0. Hence a checked0 may change to2 at most once and cannot change back.
This constraint still does not supply the actual transition times.

Pulling (9) left produces zero/nonzero conditions with the specified
time phase; it does not by itself give another copy of the same
certificate. No closed finite family of these ancestry conditions, or
cheaper construction of the required word, has been proved. On the
actual zero seed the first rows are B(0)=1^infinity and C(0)=3^infinity,
so no interior rise occurs at middle time1. A chain consisting only of
these transparent pairs cannot begin at time0.

## 4. Actual rise data do not yet advance another block

The earlier high-field reduction uses Z=D+H and the zero-padded rise
field rho_i=A_i(1+A_(i-1)), with rho_0=A_0. The following example
identifies the missing information for a causal prefix update of this
summary. It uses only the saved whole-ray certificates in the
[two-channel artifact](../../experiments/rule30/p3-b-two-channel-block.json):

```
B²(0)=2^infinity,       B⁴(0)=(03)^infinity,
B⁶(0)=(2332)^infinity,  B⁸(0)=003(0332)^infinity.
```

At old times0 and4 the whole Gray field is zero. The intermediate low
fields are respectively 1^infinity and (1001)^infinity; the latter
follows by closing the four-phase Gray low scan on the supplied B⁴ ray,
as proved in the last-rise report. Their first two bits and outcomes are

| Old time | Z prefix | A prefix | rho prefix | High at site1 after two steps | High at site1 after four steps |
|---:|---|---|---|---:|---:|
| 0 | 00 | 11 | 10 | 1 | 1 |
| 4 | 00 | 10 | 10 | 1 | 0 |

The identical length-two (Z,rho) summaries correctly determine the
first high output, but cannot determine that prefix's high output after
another block. The retained A prefixes distinguish the two cases.
This is a failure of a causal update using only those prefix summaries;
it does not identify the complete rho fields or exclude summaries with
additional information, lookahead, or actual query-dependent guards.
No new orbit is generated for this control.

## 5. Measured chain lengths do not grow with depth, and exceed a random control

Date: 2026-09-18. Before attempting to construct the section 2 certificate
cheaply, its actual usefulness was measured directly: for the real
zero-seed orbits `B^t(0)` and `C^t(0)`, at each site `i` up to `2198`, the
maximal empirical run length `K` with `high(g^(a+2K)(0))_i=high(g^a(0))_i`
for some starting time `a`, scanned over `t<=2200`. This upper-bounds what
any correct guard certificate could ever exploit, since a guard-satisfying
chain is a special case of high-bit persistence, without needing to encode
the guard language.

The measured mean `K` rises from about 7 near the origin to a plateau
around 17 by site 50, and stays at that plateau (16-18 mean, under 40
maximum) through site 2198 for both generators. The disconfirming control
is the identical scan against an i.i.d. random bit column of the same
shape: it also plateaus, at a mean around 9.5 (max 20), stable across
seeds. The real plateau is consistently about 1.8 times the random
plateau, so the real persistence is not merely a sampling artifact of a
structureless column, but it still does not grow with site index over the
tested range, unlike the random control. If this plateau is real at all
depths, no construction of this certificate, however cheap, gives more
than a constant per-query saving; it cannot alone yield a sublinear
algorithm. This is a finite scan, not a proof that `K` stays bounded for
every `n`.

The [scanner](../../experiments/rule30/p3_guard_chain_length_scan.py) and
[artifact](../../experiments/rule30/p3-guard-chain-length-scan.json) retain
the full bucketed statistics for both generators and the control.

## 6. Two further candidates, both killed

The low-bit half of the singleton query (`RESULTS-p3-actual-b-query.md`
equation 1, even index `e=0`) reduces unconditionally, with no guard, via
equation (4) above: `low(digit_i(B^N(0)))` equals the parity of
`#{s<=N: digit_(i-1)(B^s(0))!=0}`. Verified against 89,400 direct cases
with zero mismatches. This converts a point query into a counting query,
but algebraic inspection of the bitplane equations (1) shows that whether
`digit_i` of the output ray is zero depends on the **same-time** output at
site `i-1` and the same-site input from the previous time step, an
inherently two-dimensionally coupled dependency, not a telescoping
one-site count. Directly testing whether the running parity at site `i`
is a function of the running parity at site `i-2` alone confirms this: it
is mixed at every one of 80 tested sites, with zero exceptions. The exact
identity is real; it does not by itself escape the coupling. The
[probe](../../experiments/rule30/p3_count_telescope_probe.py) and
[artifact](../../experiments/rule30/p3-count-telescope-probe.json) retain
the identity check and the per-site class counts.

A multiplicative (doubling) analogue of the additive chain above,
`high(B^(2a)(0))_i = high(B^a(0))_i`, was also tested directly: the match
rate across roughly 720,000 `(site, a)` pairs is `50.11%`, indistinguishable
from a coin flip, with no site showing a rate meaningfully above chance.
Neither candidate is promoted; both are recorded here as investigation
notes in the style of
[the session-limits supplement](RESULTS-p3-session-limits-supplement.md#3-other-analyses-that-did-not-produce-a-new-cost-theorem).

## 7. Verification and construction cost

The [verifier](../../experiments/rule30/p3_rise_chain_transparency.py) and
[artifact](../../experiments/rule30/p3-rise-chain-transparency.json)
check the local transparency identity, distinct origins, complete pair
language, actual-state pullbacks, and the saved-ray comparison.

The all-length proofs above establish that a verified chain replaces K
two-time high updates by one earlier high readout. Direct certificate
checking still performs O(K) local Boolean operations on a supplied
word, with allocation and index costs charged separately. Obtaining
that actual word, its entering low bit, and the earlier high endpoint
has not been made cheaper here. A compressed accepted-run certificate
could help only with its construction and verification costs included.
The missing P3 step is a recurrence that constructs these actual
certificates while reducing total query work.
