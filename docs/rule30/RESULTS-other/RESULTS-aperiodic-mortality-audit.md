**Aperiodic zero-cost mortality: cumulative history information and two controls**

Date: 2026-09-11. No all-budget mortality theorem, repeat upper bound, or
Rule 30 prize conclusion is proved here. All frontier statements use the legal
auxiliary Z universe, not asserted lone-seed reachability.

The useful outcome of this attack is a concrete cumulative counting target
that tolerates the known repeat plateaus. A stronger version is disproved.
Two exact controls explain why periodic fixed prefixes and shallow ancestry
cannot replace the missing global argument.

**1. A cumulative information target, with its precise implication.**

Retain the original length r throughout. For a chronological scalar tape alpha,
let C_r(alpha) be the set of legal length-r frontiers whose actual Z trajectory
survives every step of alpha and emits exactly that tape. Let D(alpha) count
equal adjacent scalars. There are exactly 2^(2r-1) legal initial frontiers.

The candidate is

    |C_r(alpha)| * 2^D(alpha) <= 2^(2r-1)               (C)

for every r and every finite tape. This is UNPROVED. For empty ancestor sets
it is automatic. For nonempty sets it says

    log2(2^(2r-1) / |C_r(alpha)|) >= D(alpha).

Equivalently, a uniformly chosen legal original frontier has probability at
most 2^(-D(alpha)) of producing the specified successful tape. The probability
is an exact finite counting device; no random-seed assertion substitutes for
the required bound on every specified history.

**Conditional implication.** If (C) holds, a successful tape has at least one
ancestor, so D <= 2r-1. Substituting this into the already proved
[repeat lower bound](RESULTS-repeat-budget-lower-bound.md),

    r+N+1 <= 2^(D+1)(r+2),

gives

    N <= 4^r(r+2) - r - 1.

Thus (C) would prove mortality of every finite legal Z-frontier, and thereby
exclude eventual period two for the finite-origin Rule 30 problem. It would
not address every center period. The implication is proved; (C) is not.

More generally, any constants c>0 and epsilon>0 independent of r and alpha
such that |C_r(alpha)| <= c*2^(2r-1-epsilon*D(alpha)) would suffice. The
particular one-bit normalization in (C) is a testable choice, not a necessary
condition for mortality.

This differs from demanding a contraction at each repeat. Earlier restrictions
can accumulate information that pays for later repeats, even if those repeats
remove no original ancestors. It has not been shown easier than the original
repeat-budget problem. The sharp conjecture D<=r-1 does not, by itself, supply
the ancestor-count estimate in (C).

**2. Three repeat charges can occur while the whole ancestor set stays fixed.**

The previous [history-count report](RESULTS-fixed-origin-history-count.md)
gave two consecutive free repeats. The same 36 length-six starts give the
longer exact plateau

    C_6(101) = C_6(1011) = C_6(10111)
             = C_6(101110) = C_6(1011100),

with cardinality 36 throughout. The final tape has three repeats. This
immediately disproves the stronger two-bit version of (C):

    36 * 4^3 = 2304 > 2048 = 2^(2*6-1).

The one-bit version survives this example: 36*2^3 = 288 <= 2048. The original
set after 101 has already acquired log2(2048/36) information bits; the example
requires no new information to be acquired at the next three repeat edges.

The verifier enumerates the entire ancestor sets, records all 36 original
words, and checks every attempted update through initial length seven against
the unchanged bit-parallel frontier engine. This is a finite exact
counterexample to the two-bit estimate, not a counterexample to mortality.

One can also define the stronger aggregate candidate

    M_r(n) = sum_(|alpha|=n) |C_r(alpha)| * 2^D(alpha)
             <= 2^(2r-1).

It survived the bounded checks through r=9. However, M_r(n) is not a
nonincreasing process: M_4(1)=56 and M_4(2)=60. Thus neither an automatic
martingale argument nor stepwise ensemble descent has been established.
The aggregate bound is optional; proving (C) alone would suffice.

**3. Finite origin and periodic fixed prefixes do not force a periodic tip.**

Here is a separate control system, not a Z trajectory. Start with the finite
binary word [1]. At time t retain indices 0,...,t. Update and append by

    a_k(t+1) = a_k(t) XOR a_(k-3)(t),    0 <= k <= t+1,

using zero for missing coordinates. This is a fixed sequential scan with
three bits of memory and one-symbol growth. For every retained coordinate,

    a_k(t) = [x^k](1+x^3)^t over F_2.                 (1)

The new-coordinate boundary must be checked in proving (1). For k=t+1 the
missing old coefficient is zero: if 3 does not divide k this is immediate;
if k=3m, it equals binomial(3m-1,m) mod 2. At bit j=v_2(m), m has a one and
3m-1 has a zero, so that binomial coefficient is even. This follows directly
from the binary factorization (1+x)^n=PRODUCT_(j:n_j=1)(1+x^(2^j)) over F_2.
Thus discarding not-yet-born coordinates does not invalidate (1).

For every fixed K, choose h such that 3*2^h>K. Since

    (1+x^3)^(2^h) = 1+x^(3*2^h),

the prefix through K, once it exists, is purely periodic with period dividing
2^h. Nevertheless the moving tip z_t=a_t(t) is aperiodic. It is zero unless
t=3m, and then

    z_(3m) = binomial(3m,m) mod 2
           = 1 exactly when m & (2m) = 0.

Hence z_(3*2^j)=1 for every j. On the other hand, every tip in the interval

    9*2^j <= t < 12*2^j

is zero: at divisible-by-three times, m has leading binary digits 11 and
therefore overlaps its one-bit shift. Infinitely many ones and arbitrarily
long zero intervals exclude eventual periodicity.

This refutes the general inference even with a finite initial word, a fixed
finite-state update, one-symbol growth, and dyadic fixed-prefix periods.
The verifier checks (1), the append boundary, 7,471 prefix returns, and the
displayed tip controls through time 256. The all-time statement follows from
the algebra, not from that finite check.

A suggested repair using a single fixed return lag P and a bounded terminal
strip gives no new Z theorem. The archive already proves a temporally
P-periodic autonomous prefix has at most 4^P-1 sites. Even one exact P-step
return of an autonomous prefix makes that prefix periodic. Therefore the
return restriction already follows from the existing theorem; the difficult
regime permits growing periods and growing stabilization times.

**4. A legal reconstructed interface need not have the required ancestry.**

The exact scan gives the all-length constraint

    Z^2(legal frontiers) has no word beginning 320.

Indeed, an output beginning 320 forces its input to begin 302 or 312. Any
first image beginning 3 has second low bit zero, excluding 312. If its second
symbol is 0, its predecessor's second high bit is one, forcing the third
output low bit to be one and excluding 302. This is a direct consequence of
the existing image machinery, not a new extinction result.

For example,

    320303032 --1--> 3030303032

is an actual successful Z update. Both endpoints have legal origin and
terminal birth data. The first endpoint nevertheless cannot be a second
image, let alone the fifth image of a nominal length-four origin. Such a
formal switch interface cannot be certified by its anchor and a successful
future step. The attempted two-episode proof still needs chronological
ancestry; the candidate episode bound was neither proved nor disproved.

**5. Computation and remaining decision.**

The standalone [verifier](../../experiments/rule30/aperiodic_mortality_audit.py)
defaults to an exhaustive census through initial length nine. Its saved
[artifact](../../experiments/rule30/aperiodic-mortality-audit.json) contains
174,762 legal starts and 21,576 attempted updates independently checked against
the frozen engine through initial length seven. Time or lifetime caps raise
an error; they never become a mortality verdict.

An earlier bounded single-implementation continuation in this session also
checked lengths 10, 11, and 12 completely, in about 31 seconds total. Thus
(C) was checked on all 11,184,810 legal starts of lengths 1 through 12. The
extension is a recorded observation, not an independent second verification.
Its maxima over nonempty tapes were:

| Initial length | Maximum weighted count | Number of legal starts | Maximizing tape |
|---:|---:|---:|:---|
| 10 | 131072 | 524288 | 0 |
| 11 | 525312 | 2097152 | 1 |
| 12 | 2097152 | 8388608 | 0 |

The table reports finite maxima, not an asymptotic estimate. The maintained
verifier accepts --max-length 12 to reproduce that extension; it was not
rerun merely to repackage these values. No GPU or seed regeneration was used.

The next mathematical obligation for this candidate is a length-uniform
bound on the probability of a complete guarded history as a function of its
repeat count. Fixed-prefix periodicity, ambient inverse multiplicity, and
conditional contraction at every repeat do not supply it. This investigation
has isolated that candidate and falsified stronger shortcuts; it has not
proved the needed cumulative cancellation of possibilities.

**Follow-up, 2026-09-11.** The
[cumulative-history transfer report](RESULTS-cumulative-history-transfer.md)
proves (C) for every original length r when the tape has at most nine symbols,
using a common spatial graph and an exact maximum-principle certificate. The
sharp repeat factor on that bounded-tape class is `(2^24/24561)^(1/6)`.
It also refutes the stronger `3^D` normalization:
`|C_14(00001111)|=196488` and `196488*3^6>2^27`, with all ancestors independently
replayed through the frozen oracle. Arbitrary tape lengths, the unrestricted
positive-rate information bound, and mortality remain open.

**Further follow-up, 2026-09-11.** The
[all-depth spatial mixing report](RESULTS-history-transfer-mixing.md) proves
strong connectivity of the common transfer graph for every temporal depth n,
and `|C_r(alpha)|/2^(2r-1) -> 4^(-n)` as r grows with n fixed. It gives an
explicit spatial cutoff at every n. A separate exact nine-symbol probability
envelope proves (C) for all original lengths and all tape lengths with D<=6.
This still supplies no upper bound on D for a fixed original frontier.

**Weighted-history follow-up, 2026-09-11.** The
[weighted endpoint report](RESULTS-weighted-history-endpoints.md) refutes the
unrestricted c=1, epsilon=3/2 estimate: the tape
`00011100001111111100` has 55,885,140 original length-24 ancestors and D=15.
Eight repeats occur while its entire original ancestor set remains unchanged.
The report proves an exact weighted endpoint counting identity and, as a
corollary of the existing reconstruction, proves that after r successful
updates every further prescribed continuation either retains the whole
original class or kills it. The two counterexample counts have independent
oracle-based compressed verification. The one-bit candidate and every
unrestricted positive-rate mortality conclusion remain open.

**Visible-low-bit follow-up, 2026-09-11.** The
[constant-high-family report](RESULTS-constant-high-history-family.md) proves
the sharp uniform bounds N<=16 and D<=8 at every original length when all
nonterminal original high bits are one. All original low bits and the final
high bit are free. Complete spatial-period and guard certificates, independently
checked with the frozen oracle, cover this infinite family. The exact first-step
low-bit erasure law proves the sharp c=1, epsilon=1/8 high-row-conditioned bound
on this base case. Its proposed extension to all high rows was subsequently
refuted, as described below. The report also refutes the opposite row-by-row one-bit bound
using 1664 individually replayed originals with a fixed low row. None of these
results proves or refutes the unrestricted one-bit candidate.

**Conditional-rate obstruction, 2026-09-11.** The
[sparse-high report](RESULTS-sparse-high-history-obstruction.md) refutes the
high-row-conditioned c=1, epsilon=1/8 extension: the legal original
`2^17197 0 2^29537` emits `1100000000000111110000`, with D=18. Exactly one
quarter of all low rows with that original high row share the entire guarded
trajectory. An all-length affine-rank theorem proves that when there are two
visible original low bits, the first prescribed guarded scalar already fixes
both; every later nonempty conditional history class retains all its original
low rows. All four effective originals are independently replayed through
failure. This refutes the conditional route, not the unrestricted cumulative
counting inequality or every weaker positive-rate estimate.

**Original-variable counting follow-up, 2026-09-11.** The
[guarded BDD report](RESULTS-guarded-history-bdd.md) gives an exact seam identity
over the fixed original bits and a new symbolic counter preserving every
chronological guard. It completes all continuations of seven specified
nine-symbol history classes, including 2,248,825,019,423,562 original
length-35 frontiers with prefix `000111000`. Independent transfer counts
check all seven roots; frozen-oracle endpoint counts check every node of the
two older trees and selected new fibers. All completed classes satisfy (C).
This is restricted finite verification, not mortality for all length-35
originals or a new uniform inequality. The previous exponent obstruction is
not improved, and the unrestricted target remains open.

**Encoding obstruction, 2026-09-11.** The
[original-history encoding report](RESULTS-history-encoding-obstruction.md)
refutes two sufficient mechanisms for (C). In the length-24, D=15 class,
every injective fixed coordinate projection must retain at least 39 of the
47 original free bits, whereas a D-bit deletion would retain only 32.
The affine hull also has dimension at least 41, so at most six independent
affine equations can hold on the class. The certificate consists of 59
explicit originals, independently replayed through all guards. These are
obstructions to coordinate deletion and affine-equation rank, not to general
linear readouts, adaptive queries, nonlinear encodings, or (C) itself.

**History-locality follow-up, 2026-09-11.** The
[locality report](RESULTS-history-locality-obstruction.md) proves a uniform
gap-completion theorem for exact original histories. For a fixed length-n
tape and r>=1+(k+1)(4^(n+1)-2), every assignment to any k original free bits
occurs in its ancestor class. Thus counting envelopes made solely from
bounded-arity support predicates cannot prove any uniform positive repeat
rate. This does not refute (C). Conversely, the known length-24, D=15 class
has a concrete nonlinear six-block code with product bound 3,857,168,160<2^32;
seven-bit overlapping windows also certify (C) for that class. The report
derives the exact full-defect recurrence and rejects a defect-population
rank by an all-length switch family. Unrestricted mortality and period-two
exclusion remain open.

**Proposed average-forcing target, 2026-09-12.** The
[new hypothesis](HYPOTHESIS-average-forced-history.md) asks whether the mean
number of forced original bits in a specified right-to-left decoder is at
least D/2. A prefix-code lemma would turn this into the sufficient c=1,
epsilon=1/2 count bound. An exact reverse pair automaton computes the mean
while retaining all chronological guards. The new statistic is certified
at every original length through tape depth nine and passes on the seven
existing weighted continuation trees. A stronger minimum-path version is
refuted at r=31, tape `00000000`; the average version remains unproved.

**Average-forcing test and uniform attempt, 2026-09-12.** The
[depth-ten and lift report](RESULTS-average-forcing-lift.md) completes the
preregistered next test within its saved limits. The average-forcing
hypothesis is now certified at all original lengths for tapes through ten
symbols, using 28,672 additional transfer comparisons and a full-state tail
certificate at r=28. The stronger finite-range means, combined with the
previous six-symbol spatial tail certificate, also prove the original
exponent-one inequality for all original lengths at tape lengths at most
ten. This deduction reuses saved certificates without a new enumeration.
No greater temporal depth was tested. The subsequent all-depth argument
factors the reverse adjacency as HK and the transposed forward adjacency
as KH, proves reverse mixing, and identifies an exact tape-independent
spatial limit mu_n for the mean forced count. The temporal four-lift
partition proves mu_n is nondecreasing, but supplies no positive linear
lower rate. A fully guarded r=29 repeat decreases the conditional mean
from 13.27097... to 12.51897..., excluding monotone-mean induction while
leaving the cumulative hypothesis intact. Uniform mortality and period-two
exclusion remain open.
